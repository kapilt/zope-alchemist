"""
$Id$
"""

from zope.formlib import form
from zope.app.form import CustomWidgetFactory

from Products.alchemist.browser import formlib, objectwidget

from Products.orgpeople.interfaces import IPersonTable
from Products.orgpeople.domain import Address

class PersonView( formlib.RecordDisplayForm ):
    form_fields = form.Fields( IPersonTable, for_display=True, render_context=True )
    form_fields = form_fields.omit('person_id')
    form_fields['address'].custom_widget = CustomWidgetFactory( objectwidget.RecordDisplayWidget, Address )

class PersonEditView( formlib.RecordEditForm ):
    form_fields = form.Fields( IPersonTable )
    form_fields = form_fields.omit('person_id', 'address_id')
    form_fields['address'].custom_widget = CustomWidgetFactory( objectwidget.RecordWidget, Address )    

class PersonAddingView( formlib.RecordAddForm ):
    form_fields = form.Fields( IPersonTable, for_input=True)
    form_fields = form_fields.omit('person_id', 'address_id')
    form_fields['address'].custom_widget = CustomWidgetFactory( objectwidget.RecordWidget, Address )
    
