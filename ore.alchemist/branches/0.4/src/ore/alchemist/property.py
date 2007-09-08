##################################################################
#
# (C) Copyright 2006 ObjectRealms, LLC
# All Rights Reserved
#
# This file is part of Alchemist.
#
# Alchemist is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Alchemist is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CMFDeployment; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##################################################################
"""
Binding Zope3 Schema Properties to Alchemist Mapped Classes

$Id$
"""

from sqlalchemy.orm import attributes
from interfaces import IIModelInterface
from zope import schema

class ValidatedProperty( object ):
    """
    Computed attributes based on schema fields that collaborate with sqlalchemy
    properties, and provide validation, error messages, and default values.
    """
    def __init__(self, field, prop, name=None):
        self.__field = field
        self.__prop = prop
        self.__name = name or field.__name__
    
    def __get__(self, inst, klass):
        if inst is None:
            return self
        return self.__prop.__get__( inst, klass )

    def __getattr__(self, name):
        # delegate to sa props
        return getattr( self.__prop, name )
    
    def __set__(self, inst, value):
        field = self.__field.bind(inst)
        field.validate(value)
        if field.readonly and inst.__dict__.has_key(self.__name):
            raise ValueError(self.__name, 'field is readonly')
        self.__prop.__set__( inst, value )

    def __delete__(self, obj):
        if self.__field.readonly and inst.__dict__.has_key(self.__name):
            raise ValueError(self.__name, 'field is readonly')
        self.__prop.__delete__( obj )

def providedByInstances( klass ):
    """ return all the interfaces implemented by instances of a klass.. why isn't this in z.i?
    """
    class_provides = getattr( klass, '__provides__', None )
    if class_provides is None:
        return ()
    return iter( class_provides._implements )
    
def bindClass( klass, mapper=None ):
    """ insert validated properties into a class based on its primary mapper, and model schemas
    """
    # compile the klass mapper, this will add instrumented attributes to the class
    # we could alternatively do.. mapper.compile() compiles all extant mappers

    if mapper is None:
        mapper = getattr( klass, 'mapper')

    mapper.compile()

    # find all the model schemas implemented by the class
    for iface in providedByInstances( klass ):
        if not IIModelInterface.providedBy( iface ):
            continue

        # for any field in the schema, see if we have an sa property
        for field_name in schema.getFieldNames( iface ):
            v = klass.__dict__.get( field_name )

            # if so then wrap it in a field property
            if not isinstance( v, attributes.InstrumentedAttribute):
                continue
            field = iface[ field_name ]
            vproperty = ValidatedProperty( field, v, field_name )
            setattr( klass, field_name, vproperty )
