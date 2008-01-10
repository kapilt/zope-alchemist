"""

$Id$
"""

from zope import schema, interface
from zope.formlib import form
from zope.security import proxy
from zc.table import column
from zc.table import table

from ore.alchemist.sa2zs import queryAnnotation
from copy import deepcopy
from i18n import _

class Getter( object ):

    def __init__(self, getter):
        self.getter = getter

    def __call__( self, item, formatter):
        return self.getter( item )

def viewLink( item, formatter ):
    return '<a class="button-link" href="%s">View</a>'%item.id

def editLink( item, formatter ):
    return '<a class="button-link" href="%s/edit">Edit</a>'%item.id

def viewEditLinks( item, formatter ):
    return '%s %s'%(viewLink( item, formatter), editLink( item, formatter ) )

class ContainerListing( form.DisplayForm ):

    form_fields = form.Fields()

    def update( self ):
        context = proxy.removeSecurityProxy( self.context )
        columns = []

        domain_model = context.domain_model
        domain_interface = list( interface.implementedBy(domain_model) )[0]
        domain_annotation = queryAnnotation( domain_interface )

        field_column_names = domain_annotation and domain_annotation.listing_columns \
                             or schema.getFieldNamesInOrder( domain_interface )

        for field_name in field_column_names:
            field = domain_interface[ field_name ]
            columns.append(
                column.GetterColumn( title= ( field.title or field.__name__ ),
                                     getter = Getter( field.query ) )
                )

        columns.append(
            column.GetterColumn( title = _(u'Actions'),
                                 getter = viewEditLinks )
            )
        
        self.columns = columns

        super( ContainerListing, self).update()

    def render( self ):
        return self.index()

    def listing( self ):
        context = proxy.removeSecurityProxy( self.context )
        
        formatter = table.SortingFormatter( context,
                                            self.request,
                                            context.values(),
                                            prefix="form",
                                            visible_column_names = [c.name for c in self.columns],
                                            columns = self.columns )
        formatter.cssClasses['table'] = 'datagrid'
        formatter.table_id = "datacontents"
        return formatter()
                                              
    @form.action(_(u"Add") )
    def handle_add( self, action, data ):
        self.request.response.redirect('add')


                 

