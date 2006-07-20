"""
$Id$
"""

# zope interface decl are on the class but not useable as such
from sqlalchemy.attributes import AttributeManager, InstrumentedAttribute

def managed_attributes(self, class_):
    """returns an iterator of all InstrumentedAttribute objects associated with the given class."""
    if not isinstance(class_, type):
        raise repr(class_) + " is not a type"
    for key in dir(class_):
        value = getattr(class_, key, None)
        if isinstance(value, InstrumentedAttribute):
            yield value




AttributeManager.managed_attributes = managed_attributes
