
from zope import interface
from zope.viewlet import viewlet, manager
from zope.formlib import form
from zope.formlib.namedtemplate import NamedTemplate

from i18n import _
import core

class FormViewlet( form.SubPageForm, viewlet.ViewletBase ):

    __init__ = viewlet.ViewletBase.__init__

class EditFormViewlet( form.SubPageEditForm, viewlet.ViewletBase ):

    __init__ = viewlet.ViewletBase.__init__

    adapters = None

    def setUpWidgets( self, ignore_request=False):
        self.adapters = self.adapters or {}
        self.widgets = setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request
            )
        
    @form.action(_(u"Edit"), condition=form.haveInputWidgets)
    def handle_edit_action( self, action, data ):
        return core.handle_edit_action( self, action, data )
    
    def invariantErrors( self ):        
        errors = []
        for error in self.errors:
            if isinstance( error, interface.Invalid ):
                errors.append( error )
        return errors
            
class DisplayFormViewlet( form.SubPageDisplayForm, viewlet.ViewletBase ):
    
    __init__ = viewlet.ViewletBase.__init__

class AttributesEditViewlet( core.DynamicFields, EditFormViewlet ):

    mode = "edit"
    template = NamedTemplate('alchemist.subform')
    form_name = _(u"General")
    
class AttributesViewViewlet( core.DynamicFields, DisplayFormViewlet ):

    mode = "view"
    template = NamedTemplate('alchemist.subform')    
    form_name = _(u"General")

class ContentViewletManager( manager.ViewletManagerBase ):
    
    def sort( self, viewlets ):
        sorted( viewlets )
        #viewlets.sort( sorter )
        return viewlets
