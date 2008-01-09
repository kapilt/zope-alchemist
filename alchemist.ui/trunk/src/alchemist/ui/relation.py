"""
$Id: $

UI/Viewlets for Managing Relations 

"""

from zope import interface
from zope.formlib import form, namedtemplate
from zope.app.pagetemplate import ViewPageTemplateFile
from zc.table import table, column
from ore.alchemist import Session

import sqlalchemy as rdb
import viewlet, core

class RelationTableBaseViewlet( viewlet.FormViewlet ):

    domain_model  = None # domain model of the other end of this relationship
    property_name = None # property on context's domain model which denotes the relationship

    selection_column = column.SelectionColumn( lambda item: str(item.id), name="selection")
    
    results = () # any subclass is expected to populate as it will.
    form_fields = form.Fields()  # these as well

    @property
    def form_name( self ):
        n = self.property_name.title()
        return n.replace('_', ' ')

    @property
    def prefix( self ):
        return self.property_name

    def setUpColumns( self ):
        columns = core.setUpColumns( self.domain_model )
        return columns

    def setUpFormatter( self ):
        """ setup table listing formatter """
        columns = self.setUpColumns()

        formatter = table.StandaloneFullFormatter(
            self.context,
            self.request,
            self.results,
            prefix=self.prefix,
            columns = columns
            )

        formatter.cssClasses['table'] = 'yui-dt-table'
        return formatter
    
    def render_listing( self ):
        """
        render a listing of all the currently associated objects or
        search results.
        """
        formatter = self.setUpFormatter()
        return formatter()

class RelationStackedBaseViewlet( viewlet.FormViewlet ):
    """
    display viewlet for stacked objects
    """

class One2OneBase( core.DynamicFields ):

    template = namedtemplate.NamedTemplate('alchemist.subform')
    
    def getDomainModel( self ):
        return self.domain_model

    def getValue( self ):
        value = getattr( self.context, self.property_name, None )
        if value is None:
            # create one on the fly
            return self.domain_model()
        return value

    @property
    def prefix( self ):
        return self.property_name    

    @property
    def model_schema( self ):
        return list( interface.implementedBy(self.domain_model) )[0]

    
class One2OneDisplay( One2OneBase, viewlet.DisplayFormViewlet ):    
    form_name = "one2one display"
    mode = 'view'
    actions = ()

    notset_template = ViewPageTemplateFile('templates/one2one-unset.pt')

    def setUpWidgets( self, ignore_request=False ):
        self.adapters = { self.model_schema : self.getValue() }
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, for_display=True,
            ignore_request=ignore_request
            )

    def render( self ):
        if self.getValue() != self.getValue():
            return self.notset_template()
        return super( One2OneDisplay, self).render()
    
class One2OneEdit( One2OneBase, viewlet.EditFormViewlet ):

    form_name = 'one2one edit'
    mode = 'edit'

    def setUpWidgets( self, ignore_request=False ):
        self.adapters = { self.model_schema : self.getValue() }
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request
            )

    @form.action(u"Apply", condition=form.haveInputWidgets)
    def handle_edit_action( self, action, data):
        super( One2OneEdit, self).handle_edit_action.success( data )
        value = self.adapters[ self.model_schema ]
        # XXX we need better detection.. alternative is trying to use
        # something like an object modified event handler...
        if self.status.startswith('Updated'):
            # save or update if modified.
            Session().save_or_update( value )
            # associate to self
            setattr( self.context, self.property_name, value )            
                
class One2ManyDisplay( RelationStackedBaseViewlet ):
    """
    display viewlet for stacked objects (m) of one 2 many relation.
    """
        
class One2ManyEdit( RelationStackedBaseViewlet ):
    """
    edit viewlet for stacked objects (m) of one 2 many relation.    
    """

class Many2ManyDisplay( RelationTableBaseViewlet ):

    template = ViewPageTemplateFile('templates/relation-view.pt')
    actions = ()
    
    def update( self ):
        # populate results with values from relation
        self.results = getattr( self.context, self.property_name )
        super( Many2ManyDisplay, self).update()
        
class Many2ManyEdit( RelationTableBaseViewlet ):

    selection_column = column.SelectionColumn( lambda item: str(item.id), name="selection")
    state = 'listing'
    template = ViewPageTemplateFile('templates/relation-edit.pt')

    def setUpColumns( self ):
        columns = super( Many2ManyEdit, self).setUpColumns()
        columns.insert(0, self.selection_column )
        return columns
    
    def update( self ):

        # we capture state from the last processed action, so our next action
        # becomes available.
        self.state = self.request.get( "%s.state"%self.property_name, self.state )
        
        # our previous state when we process searches is the add state, in order
        # to process the form values for the search action, we need to have search
        # widgets setup prior to the handler invocation, so do that here..
        if self.state == 'add':
            self.form_fields = core.setUpFields( self.domain_model, mode='search')
        
        # if we're doing a listing prepopulate state before rendering so we
        # display empty results status, and for a delete do it eagerly so
        # we can check our condition
        if self.state in ( 'listing', 'delete'):
            self.results = getattr( self.context, self.property_name)

        super( Many2ManyEdit, self).update()

        # if our state changes to listing
        if not self.results and self.state == 'listing':
            self.results = getattr( self.context, self.property_name)
            
    def condition_search( self, action):
        return self.state == 'add'
    
    @form.action( u"Search", condition='condition_search')
    def handle_search( self, action, data ):
        """
        search the other end point of m2m relationship for rows to
        associate.
        """
        self.state = 'search'
        d = core.constructQuery( self.form_fields, self.domain_model, data )

        query = Session().query( self.domain_model)
        query = query.filter(
            rdb.not_( getattr( self.domain_model, 'id').in_( [ ob.id for ob in getattr( self.context, self.property_name) ] ) )
            )
        if not d:
            self.results = query.all()
            return
                  
        self.results = query.filter( *(d.values())).all()
        
    def condition_add( self, action):
        return self.state == 'listing'
        
    @form.action( u"Add", condition='condition_add')
    def handle_add( self, action, data ):
        """
        sends user to search form.
        """
        self.state = 'add'
        session = Session()
        related_count = session.query( self.domain_model).count()
        if related_count > 20:
            self.form_fields = core.setUpFields( self.domain_model, mode='search')
        else:
            self.state = 'search'
            query = session.query( self.domain_model ).filter(
                rdb.not_( getattr( self.domain_model, 'id').in_( [ ob.id for ob in getattr( self.context, self.property_name) ] ) )
              )
            self.results = query.all()
        
    def condition_delete( self, action):
        return self.state == 'listing' and self.results
    
    @form.action( u"Delete", condition='condition_delete')
    def handle_delete( self, action, data):
        """
        delete the selected items from the m2m relationship.
        """
        # reset form state
        self.state = 'listing'
        
        # first we need to dereference the selection column values into
        # objects to disassociate.
        values = core.getSelectedObjects( self.selection_column,
                                     self.request,
                                     self.domain_model )

        if not values:
            self.status = "No %s Selected"%( self.domain_model.__name__.title()+'s')
            return
        # remove objects from association
        association = getattr( self.context, self.property_name )
        for v in values:
            if v in association:
                association.remove( v )
                
        # pluralize properly
        if len(values) > 1:
            self.status = "%s Removed"%(self.domain_model.__name__.title()+'s')
        else:
            self.status = "%s Removed"%self.domain_model.__name__.title()

    def condition_associate( self, action ):
        return self.state == 'search'
        
    @form.action( u"Associate", condition='condition_associate')
    def handle_associate( self, action, data ):
        """
        associate a search result with the context.
        """
        # reset viewlet state to listing of associated objects
        self.state = 'listing'

        # first we need to dereference the selection column values into
        # objects to associate.
        values = core.getSelectedObjects( self.selection_column,
                                     self.request,
                                     self.domain_model )

        # add objects to the association
        association = getattr( self.context, self.property_name )
        for v in values:
            if v not in association:
                association.append( v )

        # pluralize properly
        if len(values) > 1:
            self.status = "%s Associated"%(self.domain_model.__name__.title()+'s')
        else:
            self.status = "%s Associated"%self.domain_model.__name__.title()
            
        # reset selection column 
        self.form_reset = True
    
    def condition_cancel( self, action):
        return self.state != 'listing'
    
    @form.action( u"Cancel", condition='condition_cancel')
    def handle_cancel( self, action, data ):
        """
        cancel the current operation and go back to the view
        """
        self.state = 'listing'

def groupedRelationGetter( item, formatter ):
    rel_types = formatter.id_reltype_map.get( item.id, () )
    return ", ".join( rel_types )
    
class GroupedMany2Many( RelationTableBaseViewlet ):

    group_name = None # name of the group
    properties = ()   # sequence of property names
    
    @property
    def form_name( self ):
        return self.group_name

    @property
    def prefix( self ):
        return self.group_name

    def setUpColumns( self ):
        columns = core.setUpColumns( self.domain_model )
        columns.append( column.GetterColumn( title="Relation",
                                             getter = groupedRelationGetter ) )
        return columns
    
    def setUpFormatter( self ):
        formatter = super( GroupedMany2Many, self ).setUpFormatter()
        formatter.id_reltype_map = self.id_reltype_map
        return formatter

    def setUpValues( self ):
        values = []
        id_reltype_map = {}
        
        for p in self.properties:
            if p.endswith('s'):
                pn = p[:-1]
            else:
                pn = p
            pvalues = getattr( self.context, p )
            for v in pvalues:
                if v.id in id_reltype_map:
                    id_reltype_map[ v.id ].append( pn )
                else:
                    id_reltype_map[ v.id ] = [pn]
                    values.append( v )
                    
        return values, id_reltype_map
    
class GroupedMany2ManyDisplay( GroupedMany2Many ):

    template = ViewPageTemplateFile('templates/relation-view.pt')
    actions = ()
    
    def update( self ):
        self.results, self.id_reltype_map = self.setUpValues()
        super( GroupedMany2ManyDisplay, self).update()
        


        
