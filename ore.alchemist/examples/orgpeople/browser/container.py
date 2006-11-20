"""
$Id$
"""

from zope.formlib import form
from ore.alchemist.manager import get_session
from zc.table import column
from zc.table import table
from Products.Five.formlib import formbase
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

class PersonContainerView( object ):
    """ view for container
    """
    def __init__(self, context, request):
        self.context, self.request = context, request

    def search( self ):
        domain_class = self.context.domain_model
        d = {}
        for name in domain_class.c.keys():
            v = self.request.form.get(name)
            if v:
                d[name] = v
        if not d:
            return []
        return self.context.query(**d)

ListingColumns = [
    column.SelectionColumn( lambda item: str(item.person_id), name='selection' ),
    column.GetterColumn( title="First Name", getter=lambda p,f: p.first_name or ''),
    column.GetterColumn( title="Last Name", getter=lambda p,f: p.last_name or ''),
    column.GetterColumn( title="Email", getter=lambda p,f: p.email or ''),
    column.GetterColumn( title="Phone", getter=lambda p,f: p.phone_number or '')            
    ]

SelectionColumn = ListingColumns[0]

class PersonContainerListing( formbase.EditFormBase ):
    """ hello world
    """
    form_fields = form.Fields()
    prefix = "plist"

    template = ZopeTwoPageTemplateFile('person_list.pt')
    
    def renderListing( self ):
        columns = ListingColumns
        formatter = table.StandaloneFullFormatter( self.context,
                                                   self.request,
                                                   self.context.values(),
                                                   prefix="form",
                                                   visible_column_names = [c.name for c in columns],
#                                                   sort_on = ( ('Last Name', False),) ,
                                                   columns = columns )
        formatter.cssClasses['table'] = 'listing'
        return formatter()

    @form.action("Add")
    def handle_add( self, action, data ):
        return self.request.RESPONSE.redirect( "./person_add.html" )

    @form.action("Edit")
    def handle_edit( self, action, data ):
        selected = self._getSelected( action, data )
        node = selected[0]
        return self.request.RESPONSE.redirect( "./%s/person_edit.html"%(node.person_id))

    @form.action("Delete")
    def handle_delete( self, action, data ):
        selected = self._getSelected( action, data )
        session = get_session()
        for object in selected:
            session.delete( object )

    def _getSelected( self, action, data ):
        selected = SelectionColumn.getSelected( self.context.values(), self.request )
        self.form_reset = True
        return selected
