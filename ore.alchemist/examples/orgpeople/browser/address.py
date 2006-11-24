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


def AddressDisplayWidget( context, request, factory, **kw):
    return AddressDisplayWidgetClass( context, request, factory, **kw).__of__( context.context )

def AddressWidget( context, request, factory, **kw):
    return AddressWidgetClass( context, request, factory, **kw).__of__( context.context )
