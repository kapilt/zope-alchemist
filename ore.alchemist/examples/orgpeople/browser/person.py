"""

$Id$
"""


from zope.formlib import form
from zope.component import getAdapter

from Products.orgpeople.interfaces import IPersonTable

from Products.Five.browser import BrowserView

from Products.Five.formlib import formbase
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

class PersonView( formbase.DisplayForm ):
    form_fields = form.Fields( IPersonTable, for_display=True, render_context=True )
    form_fields = form_fields.omit('person_id')        
    prefix = 'view'

class PersonEditView( formbase.EditFormBase ):
    form_fields = form.Fields( IPersonTable )
    form_fields = form_fields.omit('person_id', 'address_id')
    prefix = 'edit'

class PersonAddingView( formbase.AddFormBase ):
    
    form_fields = form.Fields( IPersonTable, for_input=True)
    form_fields = form_fields.omit('person_id', 'address_id')
    
    prefix = 'add'
    
    def createAndAdd(self, data):
        person = self.context.domain_model( **data )
        self._finished_add = True
        return person

    def nextURL( self ):
        return self.context.absolute_url()    
