"""
Form Lib Variants which play nice with alchemist data models
"""

from zope.schema.interfaces import IObject
from zope.formlib.i18n import _
from ore.alchemist.interfaces import ITableSchema
from ore.alchemist.manager import get_session

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
            session = get_session()
            if newvalue in session.dirty:
                changed = True
                continue

        if (newvalue is not form_field) and (field.get(adapter) != newvalue):
            changed = True
            field.set(adapter, newvalue)

    return changed
