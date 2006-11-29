"""
Form Lib Variants which play nice with alchemist data models.

random thought -- some of the work here and objectwidget for avoiding db mods
might have been easier as a failure action, at least for edits.

author - Kapil Thangavelu <hazmat@objectrealms.net>
"""

import pytz
import datetime

import zope.event
import zope.app.event.objectevent

from zope.interface.common import idatetime
from zope.schema.interfaces import IObject
from zope.component import getAdapter
from zope.formlib.i18n import _
from zope.formlib import form
from zope.app.form import CustomWidgetFactory

from sqlalchemy.orm.session import attribute_manager

from Acquisition import aq_base
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.formlib import formbase

from ore.alchemist.interfaces import ITableSchema
from ore.alchemist.manager import get_session

class RecordDisplayForm( formbase.DisplayForm ):
    template = ZopeTwoPageTemplateFile('templates/data_view.pt')
    prefix = 'view'    

class RecordEditForm( formbase.EditFormBase ):
    template = ZopeTwoPageTemplateFile('templates/data_edit.pt')    
    prefix = 'edit'

    @form.action("Apply", condition=form.haveInputWidgets)
    def handle_edit_action(self, action, data):
        # we want to use a custom applyChanges which detects subobject in place
        # edits.
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
        super( RecordEditForm, self).update( *args, **kw )
        self.request.set('portal_status_message', self.status )    

class RecordAddForm(  formbase.AddFormBase ):
    template = ZopeTwoPageTemplateFile('templates/data_edit.pt')        
    prefix = 'add'
    
    def createAndAdd(self, data):
        record = self.context.domain_model( **data )
        self._finished_add = True
        return record

    def nextURL( self ):
        return self.context.absolute_url()    


def applyChanges(context, form_fields, data, adapters=None):
    """
    the default applyChanges from formlib, doesn't play nice with subobjects
    unless a new object is created on edit, we want to edit the value in place
    so to detect value changes on subobject changes we manually introspect
    the state of the mapped object to detect changes.
    """
    if adapters is None:
        adapters = {}

    changed = False

    for form_field in form_fields:
        field = form_field.field
        # Adapt context, if necessary
        interface = field.interface
        adapter = adapters.get(interface)
        if adapter is None:
            if interface is None:
                adapter = context
            else:
                adapter = interface(context)
            adapters[interface] = adapter

        name = form_field.__name__
        newvalue = data.get(name, form_field) # using form_field as marker
        
        if IObject.providedBy( field ) and ITableSchema.providedBy( newvalue ):
            # we expunge objects from session, to prevent spurious db changes on caught
            # form exceptions. if we get to the application of form data, then we passed
            # through validation, and values should be reattached to the session, for
            # persistence.
            if not attribute_manager.is_modified( newvalue ):
                continue
            
            newvalue = aq_base( newvalue )
            session_id = getattr( newvalue, '_sa_session_id', None)
            
            if session_id is None:
                session = get_session()
                # if the object has a instance key, its being updated
                if getattr( newvalue, '_instance_key', None):
                    session._attach( newvalue )
                    # this doesn't work as well we would expect, it resets state on updates
                    # session.save_or_update( newvalue )
                    assert newvalue in session.dirty
                    changed = True
                    continue 
                # else its new
                session.save( newvalue )                    
                changed = True

        if (newvalue is not form_field) and (field.get(adapter) != newvalue):
            changed = True
            field.set(adapter, newvalue)

    return changed
