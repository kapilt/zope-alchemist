##############################################################################
#
# Copyright (c) 2006-2008 Kapil Thangavelu <kapil.foss@gmail.com>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
Author: Kapil Thangavelu <kapil.foss@gmail.com>

$Id$
"""

import zope.interface

from zope.app.keyreference.interfaces import IKeyReference
from zope.dottedname.resolve import resolve
from ore.alchemist import Session, named

def getPrimaryKey( object ):
    values = []
    marker = object()
    for column in object.c:
        if column.primary_key:
            value = getattr( object, column.name, marker )
            if value is marker or value is None:
                raise zope.app.keyreference.interfaces.NotYet( object )
            values.append( value )
    return tuple( values )

class AlchemistKeyReference( object ):

    zope.interface.implements( IKeyReference )

    key_type_id = "ore.alchemist.keyreference"

    def __init__( self, object ):
        self.klass = named( object.__class__ )
        primary_key = getPrimaryKey( object )
        if len( primary_key ) == 1:
            self.primary_key = primary_key[0]
        else:
            self.primary_key = primary_key
        
    def __call__( self ):
        klass = resolve( self.klass )
        session = Session()
        query = session.query( klass )
        return query.get( self.primary_key )

    def __hash__( self ):
        return hash( (self.klass, self.primary_key ) )

    def __cmp__( self, other ):
        if self.key_type_id == other.key:
            return cmp( ( self.klass, self.primary_key ),
                        ( other.klass, other.primary_key ) )
        return cmp( self.key_type_id, other.key_type_id )
