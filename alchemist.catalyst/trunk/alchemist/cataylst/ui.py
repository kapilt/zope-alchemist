"""
$Id: $

generate add/edit/view forms for all the content, these get stuffed in
content.py module, and are registered by hand in content.zcml

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

from zope import  interface
from zope.formlib import form
from sqlalchemy import orm, util

from ore.alchemist import named, model
from alchemist.ui import interfaces, content
import relation



########################################
# View Factories
########################################

class ModelViewFactory( object ):
    
    name_template = None
    base_view = None
    form_name = None
    
    def __call__( self, domain_model ):
        self.setUpView( domain_model )
        
    def setUpView( self, domain_model ):

        model_schema = list( interface.implementedBy(domain_model) )[0]        
        form_name = self.name_template%(domain_model.__name__)

        # allow us to selectively replace forms on a per content basis
        if getattr( content, form_name, None) is not None:
            return
        
        form_fields = form.Fields( model_schema )
        form_class = type( form_name, (self.base_view,),
                           dict( form_fields = form_fields ) )
        
        setattr( content, form_name, form_class )

class UIAddFactory( ModelViewFactory ):
    name_template = "%sAddForm"
    base_view = content.PistonAddForm 

class UIEditFactory( ModelViewFactory ):
    name_template = "%sEditForm"    
    base_view = content.ContentEditForm

class UIDisplayFactory( ModelViewFactory ):
    name_template = "%sDisplayForm"    
    base_view = content.ContentDisplayForm

########################################
# Viewlet Factories
########################################

class ModelViewletFactory( object ):
    viewlet_name_template  = None # base template for viewlet name
    base_viewlet = None # base viewlet class
    zcml_template = None # base template for zcml registration

    def __call__( self, domain_model):
        self.setUpViewlet( domain_model )

    def checkProperty( self, *args):
        raise NotImplemented

    def getPropertyExtra( self, property, config ):
        pass
    
    def setUpViewlet( self, domain_model ):
        # attributes are handled by generic viewlet, we do this for relation views

        model_schema = list( interface.implementedBy(domain_model) )[0]                
        mapper = orm.class_mapper( domain_model )
        domain_annotation = model.queryModelDescriptor( model_schema )

        for property in mapper.iterate_properties:
            if not self.checkProperty( property,  model_schema, domain_annotation):
                continue

            property_name = property.key
            viewlet_name = self.viewlet_name_template % ( domain_model.__name__, property_name.title() )
            viewlet_name = viewlet_name.replace('_', '')
            if getattr( content, viewlet_name, None):
                continue

            d = {}
            d['domain_model'] = inverse_model = property.mapper.class_ # domain model of endpoint
            d['property_name'] = property_name

            self.getPropertyExtra( property, d )
                
                

            viewlet_class = type( viewlet_name, (self.base_viewlet,), d )
            #zcml_snippet = self.zcml_template%(
            #    "%s.%s"%(domain_model.__name__, property_name),
            #    named( model_schema ),
            #    viewlet_name
            #    )
            setattr( content, viewlet_name, viewlet_class )

    

class UIDisplayOne2OneFactory( ModelViewletFactory ):

    viewlet_name_template = "%s%sView"
    base_viewlet = relation.One2OneDisplay
    zcml_template = zcml_display_viewlet_template

    def getPropertyExtra( self, property, config ):
        inverse_schema = list( interface.implementedBy( config['domain_model'] ) )[0]
        inverse_annotation = model.queryModelDescriptor( inverse_schema )
        if inverse_annotation and getattr( inverse_annotation,'display_name', None):
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

    viewlet_name_template = "%s%sEdit"
    base_viewlet = relation.One2OneEdit
    zcml_template = zcml_edit_viewlet_template

    
class UIDisplayMany2ManyFactory( ModelViewletFactory ):

    viewlet_name_template  = "%s%sView"
    base_viewlet = relation.Many2ManyDisplay     
    zcml_template = zcml_display_viewlet_template    

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

    viewlet_name_template  = "%s%sEdit"
    base_viewlet = relation.Many2ManyEdit    

    zcml_template = zcml_edit_viewlet_template

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
    
    name_template = "%sDisplayForm"
    viewlet_name_template  = "%s%sView"
    base_viewlet = relation.GroupedMany2ManyDisplay
    zcml_template = zcml_display_viewlet_template

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
    
ui_factories = [ UIAddFactory(),
                 UIEditFactory(),
                 UIDisplayFactory(),
                 UIDisplayOne2OneFactory(),
                 UIEditOne2OneFactory(),
                 UIDisplayMany2ManyFactory(),
                 UIEditMany2ManyFactory(),                 
                 UIDisplayGroupedMany2Many()]

for domain_model in meta.models:
    
    for ui_factory in ui_factories:
        try:
            ui_factory( domain_model )
        except:
            import traceback, pdb, sys
            traceback.print_exc()
            pdb.post_mortem( sys.exc_info()[-1] )

        
