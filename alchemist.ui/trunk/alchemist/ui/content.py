"""
Generic Content Views

"""

from zope.event import notify
from zope.formlib import form
from zope.lifecycleevent import ObjectCreatedEvent
from zope.security.proxy import removeSecurityProxy
from zope.traversing.browser import absoluteURL
from zope.publisher.browser import BrowserView

from zope.app.pagetemplate import ViewPageTemplateFile

from ore.alchemist import Session
from sqlalchemy import orm

from i18n import _
import generic, core

class ContentAddForm( core.DynamicFields, form.AddForm ):
    """
    generic add form for db content
    """
    
    mode = "add"
    _next_url = None
    
    def createAndAdd( self, data ):

        domain_model = removeSecurityProxy( self.context.domain_model )
        # create the object, inspect data for constructor args      
        try:  
            ob = generic.createInstance( domain_model, data )
        except TypeError:
            ob = domain_model()
        
        # apply any context values
        self.finishConstruction( ob )
        
        # apply extra form values
        form.applyChanges( ob, self.form_fields, data )
        
        # save the object, id is generated by db on flush
        self.context[''] = ob
        
        # flush so we have database id
        session = Session()
        session.flush()
        
        # fire an object created event
        notify(ObjectCreatedEvent(ob))
        
        # signal to add form machinery to go to next url
        self._finished_add = True

        mapper = orm.object_mapper( ob )
        
        # TODO single primary key ( need changes to base container)
        oid = mapper.primary_key_from_instance( ob )[0]
        
        # retrieve the object with location and security information
        return self.context[ oid ]
        
    def finishConstruction(self, ob ):
        """ no op, subclass to provide additional initialization behavior"""
        return 
        
    def nextURL( self ):
        if not self._next_url:
            return absoluteURL( self.context, self.request )
        return self._next_url
        
    def update( self ):
        self.status = self.request.get('portal_status_message','')
        super( ContentAddForm, self).update()
        
    @form.action(_(u"Save and continue editing"), condition=form.haveInputWidgets, validator='validateUnique')
    def handle_add_edit( self, action, data ):
        ob = self.createAndAdd( data )
        name = self.context.domain_model.__name__
        self._next_url = absoluteURL( ob, self.request ) + "/@@edit?portal_status_message=%s Added"%name
        
    @form.action(_(u"Save and add another"), condition=form.haveInputWidgets)
    def handle_add_and_another(self, action, data ):
        self.createAndAdd( data )
        name = self.context.domain_model.__name__
        self._next_url = absoluteURL( self.context, self.request ) + '/@@add?portal_status_message=%s Added'%name
        
        
class ContentDisplayForm( BrowserView ):
    """
    Content Display
    """
    template = ViewPageTemplateFile('templates/content-view.pt')
    form_name = _("View")    
    
    def __call__( self ):
        return self.template()
        
class ContentEditForm( BrowserView ):
    """
    Content Edit View
    """
    template = ViewPageTemplateFile('templates/content-edit.pt')
    form_name = _("Edit")
    
    def __call__( self ):
        return self.template()
