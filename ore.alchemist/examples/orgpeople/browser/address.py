"""
$Id$
"""
from zope.interface import implements
from zope.app.form.utility import setUpWidgets
from zope.app.form.interfaces import IDisplayWidget
from Products.Five.form.objectwidget import ObjectWidgetClass, ObjectWidgetView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

class AddressWidgetView( ObjectWidgetView ):
    template = ZopeTwoPageTemplateFile('objectwidget.pt')

class ObjectDisplayWidgetClass( ObjectWidgetClass ):
    # hijack object widget edit implementation for display
    implements( IDisplayWidget )
    
    def noImplements( self, *args, **kw):
        raise NotImplemented

    def _setUpEditWidgets( self ):
        setUpWidgets(self, self.context.schema, IDisplayWidget,
                         prefix=self.name, names=self.names,
                         context=self.context)

    applyChanges = getInputValue = hasInput = hasValidInput = noImplements

class AddressDisplayWidgetClass( ObjectDisplayWidgetClass ):

    def __init__(self, *args, **kw ):
        super( AddressDisplayWidgetClass, self).__init__( *args, **kw )
        self.view = AddressWidgetView( self, self.request )


class AddressWidgetClass( ObjectWidgetClass ):
    def __init__(self, *args, **kw):
        super( AddressWidgetClass, self ).__init__( *args, **kw )
        self.view = AddressWidgetView( self, self.request )

    def getInputValue( self, *args, **kw ):
        # hmmm.. formlib doesn't call apply changes, it always setups a new value
        # on edits, try to make things update in place when a subobject value is present,
        # by calling directly to applyChanges
    
        content = self.context.context
        changes = super( AddressWidgetClass, self).applyChanges( content )
        value = self.context.get( content )
        return value

def AddressDisplayWidget( context, request, factory, **kw):
    return AddressDisplayWidgetClass( context, request, factory, **kw).__of__( context.context )

def AddressWidget( context, request, factory, **kw):
    return AddressWidgetClass( context, request, factory, **kw).__of__( context.context )
