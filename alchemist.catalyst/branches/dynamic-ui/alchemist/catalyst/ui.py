"""
$Id: $

dynamic base classes for add/edit/view forms.

todo..

 - we want to add new columns to person view ( name ) as concatenation of
   first and last name, and make it into a link to the person.

   we need to deal with global ordering on this.

 - grouped viewlets, when we have multiple m2m relations between two models,
   it would be nice to render the sets together and to allow for them

 - richer relation viewlets, we we have

 - stacked viewlets.

 - use mason model, and bind directly to zcml actions.

ajax todo..

 - ajax wants to render partial values in place, we need better selectors.
 
 """

from zope import interface
from zope.dottedname.resolve import resolve
from zope.formlib import form
from zope.security.proxy import removeSecurityProxy
from zope.proxy import removeAllProxies
from sqlalchemy import orm, util

from ore.alchemist import named, model, interfaces as irdb
from alchemist.ui import interfaces, content, relation
from alchemist.ui.core import setUpFields

from zope.formlib.interfaces import ISubPageForm
from zope.formlib.namedtemplate import NamedTemplate
from zope.app.publisher.browser.viewmeta import page
from zope.viewlet.metaconfigure import viewletDirective
from zope.app.publisher.browser.fields import MenuField

class BaseForm(object):
    name_template = "%sForm"
    template = NamedTemplate('alchemist.form')

    additional_form_fields = form.Fields()

    status = None
    mode = None
    
    @property
    def domain_model(self):
        return removeSecurityProxy(self.context).__class__

    @property
    def model_schema(self):
        return tuple(interface.implementedBy(self.domain_model))[0]

    def get_form_fields(self):
        return setUpFields(self.domain_model, self.mode)
   
    def _get_form_fields(self):
        try:
            fields = self.__dict__['form_fields']
        except KeyError:
            fields = self.__dict__['form_fields'] = self.get_form_fields()
        return fields
    
    def _set_form_fields(self, form_fields):
        self.__dict__['form_fields'] = form_fields
        
    form_fields = property(_get_form_fields, _set_form_fields)
    
class AddForm(BaseForm, content.ContentAddForm):
    mode = "add"
    defaults = {}
    
    @property
    def domain_model(self):
        return removeSecurityProxy(self.context).domain_model

    def update( self ):
        for name, value in self.defaults.items():
            self.form_fields[name].field.default = value
            
        super(AddForm, self).update()

class EditForm(BaseForm, content.EditForm):
    mode = "edit"

class DisplayForm(content.ContentDisplayForm):
    pass

########################################
# View Factories
########################################

class ModelViewFactory( object ):
    
    name_template = None
    base_view = None
    
    menu = MenuField()
    
    def __init__( self, context ):
        self.context = context
        
    def __call__( self, domain_model ):
        self.setUpView( domain_model )
        
    def setUpView( self, domain_model ):

        model_schema = list( interface.implementedBy(domain_model) )[0]        
        form_name = self.name_template%(domain_model.__name__)

        msg = ( self.name,
                self.context.ui_module.__name__,
                form_name )
                
        # allow us to selectively replace forms on a per content basis
        if getattr( self.context.ui_module, form_name, None) is not None:
            self.context.logger.debug( 
                "%s: skipped %s view %s.%s"%( domain_model.__name__, 
                                                self.name, 
                                                self.context.ui_module.__name__,
                                                form_name )
                                                
                )            
            return
        
        form_fields = form.Fields( model_schema )
        form_class = type( form_name, (self.base_view,),
                           dict( form_fields = form_fields ) )
        
        if self.context.echo:
            self.context.logger.debug( 
                "%s: generated %s view %s.%s"%( domain_model.__name__, 
                                                self.name, 
                                                self.context.ui_module.__name__,
                                                form_name )
                                                
                )

        setattr( self.context.ui_module, form_name, form_class )
        self.setUpZCML( form_name, form_class, model_schema )
        
    def setUpZCML( self, form_name, form_class, model_schema):
        if self.context.echo:
            self.context.logger.debug("%s: registered %s for %s, layer %s, permission %s"%( 
                self.context.domain_model.__name__,
                form_name,
                model_schema.__name__,
                "Default", 
                self.permission ) )
        page( self.context.zcml, self.name, self.permission, model_schema,
              class_=form_class )


class UIAddFactory( ModelViewFactory ):
    name = "add"
    permission = "zope.Public"
    name_template = "%sAddForm"
    
    base_view = content.ContentAddForm 
    
    def setUpZCML( self, form_name, form_class, model_schema):
        super( UIAddFactory, self).setUpZCML( form_name,  form_class, self.context.container_interface )
                                              

class UIEditFactory( ModelViewFactory ):
    name = "edit"
    permission = "zope.Public"
    name_template = "%sEditForm"    

    base_view = content.ContentEditForm

class UIDisplayFactory( ModelViewFactory ):
    name = "view"
    permission = "zope.Public"    
    name_template = "%sDisplayForm"    
    
    base_view = content.ContentDisplayForm

########################################
# Viewlet Factories
########################################

class ModelViewletFactory( object ):

    viewlet_name_template  = None # base template for viewlet name
    base_viewlet = None # base viewlet class
    permission = "zope.Public"
    
    def __init__( self, context ):
        self.context = context
        
    def __call__( self, domain_model):
        self.setUpViewlet( domain_model )

    def checkProperty( self, *args):
        raise NotImplemented

    def getPropertyExtra( self, property, config ):
        pass
    
    def setUpViewlet( self, domain_model ):
        # attributes are handled by generic viewlet, we do this for relation views
        ctx = self.context
        
        for property in ctx.mapper.iterate_properties:
            if not self.checkProperty( property,  ctx.domain_interface, ctx.descriptor ):
                continue
            property_name = property.key
            viewlet_name = self.viewlet_name_template % ( ctx.domain_model.__name__, property_name.title() )
            viewlet_name = viewlet_name.replace('_', '')

            msg = ( domain_model.__name__, 
                    self.name,
                    self.context.ui_module.__name__,
                    viewlet_name )            
                            
            if getattr( ctx.ui_module, viewlet_name, None):
                self.context.logger.debug( "%s: skipped %s viewlet %s.%s"%msg)
                continue

            inverse_model = property.mapper.class_ # domain model of endpoint
            if len(tuple(interface.implementedBy(inverse_model))) == 0:
                # do not create viewlet for models which do not
                # implement a schema
                continue
            
            d = {}
            d['domain_model'] = inverse_model
            d['form_name'] = inverse_model.__name__
            d['property_name'] = property_name
            
            self.getPropertyExtra( property, d )
                
            viewlet_class = type( viewlet_name, (self.base_viewlet,), d )
            #ctx.relations[ "%s-%s"%( property.key, self.name )] = viewlet_class
            setattr( ctx.ui_module, viewlet_name, viewlet_class )

            if self.context.echo:
                self.context.logger.debug( "%s: generated %s viewlet %s.%s"%msg )

            permission = d.get('permission') or self.permission
                
            self.setUpZCML( viewlet_name, viewlet_class, 
                            ctx.domain_interface, permission )
            
    def setUpZCML( self, viewlet_name, viewlet_class, domain_interface, permission  ):
        
        if self.context.echo:
            self.context.logger.debug("%s: registered %s for %s, layer %s, permission %s"%( 
                    self.context.domain_model.__name__,
                    viewlet_name,
                    domain_interface.__name__,
                    "Default", 
                    permission ) )

        viewletDirective(
             self.context.zcml, 
             viewlet_name, 
             permission,
             manager=self.viewlet_manager,
             for_=domain_interface, 
             class_=viewlet_class
             )

class UIDisplayOne2OneFactory( ModelViewletFactory ):

    name = 'display'
    viewlet_name_template = "%s%sView"
    base_viewlet = relation.One2OneDisplay
    viewlet_manager = resolve('alchemist.ui.interfaces.IContentViewManager')

    def getPropertyExtra( self, property, config ):
        inverse_schema = list( interface.implementedBy( config['domain_model'] ) )[0]
        inverse_annotation = model.queryModelDescriptor( inverse_schema )
        #if self.context.echo:
        #    print 'i', config['domain_model'], inverse_schema, inverse_annotation
        if inverse_annotation and getattr( inverse_annotation,'display_name', None):
        #    print "found form name"
            config['form_name'] = inverse_annotation.display_name

    def checkProperty( self, property, model_schema, descriptor ):
        # check thats its a scalar property
        if isinstance( property, orm.ColumnProperty):
            return False
        property_name = property.key
        if property_name in model_schema:
            return False            
        if property.uselist:
            return False
        return True
    
class UIEditOne2OneFactory( UIDisplayOne2OneFactory ):

    name = 'edit'
    viewlet_name_template = "%s%sEdit"
    base_viewlet = relation.One2OneEdit
    viewlet_manager = resolve('alchemist.ui.interfaces.IContentEditManager')    
    
class UIDisplayMany2ManyFactory( ModelViewletFactory ):

    name = 'display'
    viewlet_name_template  = "%s%sView"
    base_viewlet = relation.Many2ManyDisplay
    viewlet_manager = resolve('alchemist.ui.interfaces.IContentViewManager')         

    def __call__( self, domain_model):
        self.setUpViewlet( domain_model )

    def checkProperty( self, property, model_schema, descriptor ):
        if isinstance( property, orm.ColumnProperty):
            return False
        property_name = property.key
            
        if property_name in model_schema:
            return False            

        if not property.secondary or not property.uselist:
            return False            
        
        # check if its a grouped m2m, if so skip it
        if descriptor and property_name in descriptor:
            descriptor = descriptor.get( property_name )
            if descriptor.group:
                return False
        return True
    
class UIEditMany2ManyFactory( UIDisplayMany2ManyFactory ):

    name = 'edit'
    viewlet_name_template  = "%s%sEdit"
    base_viewlet = relation.Many2ManyEdit    

    def checkProperty( self, property, model_schema, descriptor ):
        if isinstance( property, orm.ColumnProperty):
            return False
        property_name = property.key
            
        if property_name in model_schema:
            return False            

        if not property.secondary or not property.uselist:
            return False            

        return True

class UIDisplayGroupedMany2Many( ModelViewletFactory ):
    
    name = 'display'
    name_template = "%sDisplayForm"
    viewlet_name_template  = "%s%sView"
    base_viewlet = relation.GroupedMany2ManyDisplay

    def __call__( self, domain_model):
        self.setUpViewlet( domain_model )

    def checkProperty( self, property, model_schema, descriptor ):
        if isinstance( property, orm.ColumnProperty):
            return False
        property_name = property.key
            
        if property_name in model_schema:
            return False            

        if not property.secondary or not property.uselist:
            return False            
        
        # check if its a grouped m2m, if so skip it
        if descriptor and property_name in descriptor:
            descriptor = descriptor.get( property_name )
            if descriptor.group:
                return True

        return False
    
    def setUpViewlet( self, domain_model ):
        model_schema = list( interface.implementedBy(domain_model) )[0]                
        mapper = orm.class_mapper( domain_model )
        domain_annotation = model.queryModelDescriptor( model_schema )

        grouped = util.OrderedDict()
        
        for property in mapper.iterate_properties:
            if not self.checkProperty( property, model_schema, domain_annotation ):
                continue

            property_name = property.key
            descriptor = domain_annotation.get( property_name )
            if descriptor.group in grouped:
                grouped[ descriptor.group ].append( property_name )
            else:
                grouped[ descriptor.group ] = [ property_name ]

        for group in grouped:
            
            viewlet_name = self.viewlet_name_template % ( domain_model.__name__, group )            
            viewlet_name.replace('_', '')
            
            if getattr( content, viewlet_name, None):
                continue

            inverse_model = mapper.get_property( grouped[group][0] ).mapper.class_
            d = dict( group_name = group, properties=grouped[group], domain_model=inverse_model)
            viewlet_class = type( viewlet_name, (self.base_viewlet,), d )
            
            zcml_snippet = self.zcml_template%(
                "%s.%s"%(domain_model.__name__, group),
                named( model_schema ),
                viewlet_name
                )
            
            setattr( content, viewlet_name, viewlet_class )
    
ui_factories = [ UIAddFactory,
                 UIEditFactory,
                 UIDisplayFactory,
                 UIDisplayOne2OneFactory,
                 UIEditOne2OneFactory,
                 UIDisplayMany2ManyFactory,
                 UIEditMany2ManyFactory,                 
#                 UIDisplayGroupedMany2Many
                ]

def GenerateViews( ctx ):
    if ctx.ui_module is None:
        ispec = ctx.domain_model.__module__.rsplit('.',1)[0]+'.browser'
        ctx.ui_module = resolve( ispec )    
    
    for ui_factory in ui_factories:
        maker = ui_factory( ctx )
        maker( ctx.domain_model )

