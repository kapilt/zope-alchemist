
from zope.viewlet import viewlet, manager
from zope.formlib import form
from zope.formlib.namedtemplate import NamedTemplate

import core

class FormViewlet( form.SubPageForm, viewlet.ViewletBase ):

    __init__ = viewlet.ViewletBase.__init__

class EditFormViewlet( form.SubPageEditForm, viewlet.ViewletBase ):

    __init__ = viewlet.ViewletBase.__init__

    @form.action("Apply", condition=form.haveInputWidgets)
    def handle_edit_action( self, action, data ):
        return core.handle_edit_action( self, action, data )
    
class DisplayFormViewlet( form.SubPageDisplayForm, viewlet.ViewletBase ):
    
    __init__ = viewlet.ViewletBase.__init__

class AttributesEditViewlet( core.DynamicFields, EditFormViewlet ):

    mode = "edit"
    template = NamedTemplate('alchemist.subform')
    form_name = u"General"
    
class AttributesViewViewlet( core.DynamicFields, DisplayFormViewlet ):

    mode = "view"
    template = NamedTemplate('alchemist.subform')    
    form_name = u"General"

class AlchemistViewletManager( manager.ViewletManagerBase ):
    
    def sort( self, viewlets ):
        sorted( viewlets )
        #viewlets.sort( sorter )
        return viewlets
