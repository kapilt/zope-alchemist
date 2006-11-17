"""

$Id$
"""


from zope.formlib import form
from zope.component import getAdapter

from interfaces import IPersonTable

from Products.Five.browser import BrowserView

from Products.Five.formlib import formbase
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

class PersonView( formbase.DisplayForm ):
    form_fields = form.Fields( IPersonTable, for_display=True, render_context=True )
    form_fields = form_fields.omit('person_id')        
    prefix = 'person_view'    

class PersonAddingView( formbase.AddFormBase ):
    
    form_fields = form.Fields( IPersonTable, for_input=True)
    form_fields = form_fields.omit('person_id', 'address_id')
    
    prefix = 'person_add'
    
    def createAndAdd(self, data):
        person = self.context.domain_model( **data )
        self._finished_add = True
        return person

    def nextURL( self ):
        return self.context.absolute_url()    
