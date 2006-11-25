"""
$Id$
"""

import copy
from zope.formlib import form
from zope import schema
from zc.table import column
from zc.table import table

from ore.alchemist.manager import get_session

from Products.Five.formlib import formbase
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from Products.orgpeople.interfaces import IPersonTable

#################################
# Table Columns

def idLink( person, formatter ):
    return '<a href="%s">%s</a>'%(person.absolute_url(), person.person_id)
    
SearchColumns = [
    column.GetterColumn( title="Id", getter=idLink),    
    column.GetterColumn( title="First Name", getter=lambda p,f: p.first_name or ''),
    column.GetterColumn( title="Last Name", getter=lambda p,f: p.last_name or ''),
    column.GetterColumn( title="Email", getter=lambda p,f: p.email or ''),
    column.GetterColumn( title="Phone", getter=lambda p,f: p.phone_number or '')
    ]

ListingColumns = list(SearchColumns)

SelectionColumn = column.SelectionColumn( lambda item: str(item.person_id), name='selection' )

ListingColumns.insert(0, SelectionColumn )

def searchFields( iface ):
    fields = []
    for name, field in schema.getFieldsInOrder( iface ):
        if field.required:
            field = copy.deepcopy( field )
            field.required = False
        fields.append( field )
    return fields

#################################
# Views

class PersonSearchView( formbase.FormBase ):
    """ person searching view """

    form_fields = form.Fields( *searchFields( IPersonTable ) )
    form_fields = form.Fields( form_fields, for_input=True)
    form_fields = form_fields.omit('person_id', 'address_id', 'created', 'address')
    template = ZopeTwoPageTemplateFile('person_search.pt')
    results = None
    
    @form.action("Search", condition=form.haveInputWidgets)
    def handle_search( self, action, data ):
        self.results = self.search( data )

    def search( self, data ):
        domain_class = self.context.domain_model
        d = {}
        for name in domain_class.c.keys():
            v = data.get(name)
            if v:
                d[name] = v
        if not d:
            return []
        return self.context.query(**d)

    def renderResults( self ):
        columns = SearchColumns
        formatter = table.StandaloneFullFormatter( self.context,
                                                   self.request,
                                                   self.results or (),
                                                   prefix="form",
                                                   visible_column_names = [c.name for c in columns],
                                                   columns = columns )
        formatter.cssClasses['table'] = 'listing'
        return formatter()

class PersonContainerListing( formbase.EditFormBase ):
    """ person listing view """
    
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
        return self.request.RESPONSE.redirect( "./add" )

    @form.action("Edit")
    def handle_edit( self, action, data ):
        selected = self._getSelected( action, data )
        node = selected[0]
        return self.request.RESPONSE.redirect( "./%s/edit"%(node.person_id))

    @form.action("Delete")
    def handle_delete( self, action, data ):
        selected = self._getSelected( action, data )
        session = get_session()
        for object in selected:
            session.delete( object )
        # we need to flush the session explicitly now
        session.flush()

    def _getSelected( self, action, data ):
        selected = SelectionColumn.getSelected( self.context.values(), self.request )
        self.form_reset = True
        return selected
