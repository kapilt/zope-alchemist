"""
Object Widget Improvements for Alchemist Models - aka RecordWidgets

- adds a display record widget that uses IDisplayWidget instead of the
  default object widget IInputWidget (wacky..)

- modified edit widget class which on getinputvalue, updates an existing
  value in place, instead of creating a new one.
  
$Id$
"""

from zope.interface import implements
from zope.app.form.utility import setUpWidgets
from zope.app.form.interfaces import IDisplayWidget

from Products.Five.form.objectwidget import ObjectWidgetClass, ObjectWidgetView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from ore.alchemist.interfaces import ITableSchema

class RecordWidgetView( ObjectWidgetView ):
    template = ZopeTwoPageTemplateFile('templates/objectwidget.pt')

class RecordDisplayWidgetClass( ObjectWidgetClass ):
    # hijack object widget edit implementation for display
    implements( IDisplayWidget )

    def __init__(self, *args, **kw ):
        super( RecordDisplayWidgetClass, self).__init__( *args, **kw )
        self.view = RecordWidgetView( self, self.request )
    
    def noImplements( self, *args, **kw):
        raise NotImplemented

    def _setUpEditWidgets( self ):
        setUpWidgets(self, self.context.schema, IDisplayWidget,
                         prefix=self.name, names=self.names,
                         context=self.context)

    applyChanges = getInputValue = hasInput = hasValidInput = noImplements

class RecordWidgetClass( ObjectWidgetClass ):
    def __init__(self, *args, **kw):
        super( RecordWidgetClass, self ).__init__( *args, **kw )
        self.view = RecordWidgetView( self, self.request )

    def getInputValue( self ):
        # hmmm.. formlib doesn't call apply changes, it always setups a new value
        # on edits, try to make things update in place when a subobject value is present,
        # by calling directly to applyChanges
        content = self.context.context
        # XXX hmm on adding views we content is the container, try to detect this and dispatch
        # appropriately, this is problematic on nested alchemist schemas. ideal might be
        # separate addrecordwidgetclass.
        if ITableSchema.providedBy( content ):
            changes = super( RecordWidgetClass, self).applyChanges( content )
            value = self.context.get( content )
        else:
            value = super( RecordWidgetClass, self).getInputValue()
        return value

def RecordDisplayWidget( context, request, factory, **kw):
    return RecordDisplayWidgetClass( context, request, factory, **kw).__of__( context.context )

def RecordWidget( context, request, factory, **kw):
    return RecordWidgetClass( context, request, factory, **kw).__of__( context.context )
