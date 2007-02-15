"""
Object Widget Improvements for Alchemist Models - aka RecordWidgets

- adds a display record widget that uses IDisplayWidget instead of the
  default object widget IInputWidget (wacky..)

- modified edit widget class which on getinputvalue, updates an existing
  value in place, instead of creating a new one.

- applychanges is incompatible with formlib,

- takes special care to detach objects from sa session before modification, so
  caught form errors don't trigger db modifications on txn commit.
  
$Id$
"""

from zope.interface import implements
from zope.app.form.utility import setUpWidgets, applyWidgetsChanges
from zope.app.form.interfaces import IDisplayWidget, WidgetsError

from Products.Five.form.objectwidget import ObjectWidgetClass, ObjectWidgetView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from ore.alchemist.manager import get_session
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
        # because we're modifying the subobject, and we may have errors on the form,
        # either the subobject form or the containing form, we detach newly created instances
        # from the session till the value is assigned, so we don't get any spurious db changes or db errors
        # on form errors. sa automatically takes care of reattaching to the session when we
        # store on context. nice ;-)
        self._factory = factory = self.factory
        def record_factory( self=self):
            value = self._factory()
            get_session().expunge( value )
            return value
        self.factory = record_factory

    def _applyChanges( self, content ):
        # pull in a version which expires existing values before mods
        # and which does not do a field set on the content.
        field = self.context
        value = field.query(content, None)
        if value is None:
            # create our new object value
            # TODO: ObjectCreatedEvent here would be nice
            value = self.factory()
        else:
            # detach existing from session while modifying, so if form error, we don't commit.
            get_session().expunge( value )

        # apply sub changes, see if there *are* any changes
        # TODO: ObjectModifiedEvent here would be nice
        changes = applyWidgetsChanges(self, field.schema, target=value,
                                      names=self.names)
        if changes: # modify the bound field
            field.changed = True
        return value
    
    def getContextInputValue( self, content ):
        """ update or create value on context 
        """
        # some bit rot in zope.app.form.. basically raises errors
        # wrapped up in an error container, which isn't caught. catch and unwrap.        
        try:
            return self._applyChanges( content )
        except WidgetsError, econtainer:
            self._error = {}
            for error in econtainer.args:
                self._error[ error.field_name ] = error
            raise econtainer.args[0]

    def getInputValue( self ):
        # hmmm.. formlib doesn't call apply changes, it always setups a new value
        # on edits, try to make things update in place when a subobject value is present,
        # by calling directly to applyChanges

        content = self.context.context
        # XXX hmm on adding views we content is the container, try to detect this and dispatch
        # appropriately, this is problematic on nested alchemist schemas. ideal might be
        # separate addrecordwidgetclass.

        if ITableSchema.providedBy( content ):
            value = self.getContextInputValue( content )
        else:
            # create value in vacuum ( no parent object )
            value = super( RecordWidgetClass, self).getInputValue()
        return value
    
def RecordDisplayWidget( context, request, factory, **kw):
    return RecordDisplayWidgetClass( context, request, factory, **kw).__of__( context.context )

def RecordWidget( context, request, factory, **kw):
    return RecordWidgetClass( context, request, factory, **kw).__of__( context.context )
