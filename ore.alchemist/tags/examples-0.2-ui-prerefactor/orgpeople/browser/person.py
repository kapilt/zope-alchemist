"""

$Id$
"""

import pytz
import datetime

import zope.event
import zope.app.event.objectevent
from zope.formlib.i18n import _
from zope.interface.common import idatetime
from zope.app.form import CustomWidgetFactory
from zope.formlib import form
from zope.component import getAdapter

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.formlib import formbase

from Products.alchemist.browser.formlib import applyChanges
from Products.orgpeople.interfaces import IPersonTable
from Products.orgpeople.domain import Address

from address import AddressWidget, AddressDisplayWidget

class PersonView( formbase.DisplayForm ):
    form_fields = form.Fields( IPersonTable, for_display=True, render_context=True )
    form_fields = form_fields.omit('person_id')
    form_fields['address'].custom_widget = CustomWidgetFactory( AddressDisplayWidget, Address )
    template = ZopeTwoPageTemplateFile('person_view.pt')
    prefix = 'view'

class PersonEditView( formbase.EditFormBase ):
    form_fields = form.Fields( IPersonTable )
    form_fields = form_fields.omit('person_id', 'address_id')
    form_fields['address'].custom_widget = CustomWidgetFactory( AddressWidget, Address )    
    template = ZopeTwoPageTemplateFile('person_edit.pt')    
    prefix = 'edit'

    @form.action("Apply", condition=form.haveInputWidgets)
    def handle_edit_action(self, action, data):
        if applyChanges(self.context, self.form_fields, data, self.adapters):
            zope.event.notify(
                zope.app.event.objectevent.ObjectModifiedEvent(self.context))
            formatter = self.request.locale.dates.getFormatter(
                'dateTime', 'medium')

            try:
                time_zone = idatetime.ITZInfo(self.request)
            except TypeError:
                time_zone = pytz.UTC

            status = _("Updated on ${date_time}",
                       mapping={'date_time':
                                formatter.format(
                                   datetime.datetime.now(time_zone)
                                   )
                        }
                       )
            self.status = status
        else:
            self.status = _('No changes')

    def update( self, *args, **kw):
        super( PersonEditView, self).update( *args, **kw )
        self.request.set('portal_status_message', self.status )

class PersonAddingView( formbase.AddFormBase ):
    form_fields = form.Fields( IPersonTable, for_input=True)
    form_fields = form_fields.omit('person_id', 'address_id')
    form_fields['address'].custom_widget = CustomWidgetFactory( AddressWidget, Address )
    template = ZopeTwoPageTemplateFile('person_add.pt')        
    prefix = 'add'
    
    def createAndAdd(self, data):
        person = self.context.domain_model( **data )
        self._finished_add = True
        return person

    def nextURL( self ):
        return self.context.absolute_url()    
