##################################################################
#
# (C) Copyright 2006-2007 Kapil Thangavelu <kapilt at gmail.com>
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
Author: Kapil Thangavelu <kapilt@gmail.com>

$Id$
"""

import zope.interface
import zope.app.keyreference.interfaces
from zope.dottedname.resolve import resolve

from ore.alchemist.manager import get_session
from ore.alchemist import named

def getPrimaryKey( object ):
    values = []
    marker = object()
    for column in object.c:
        if column.primary_key:
            value = getattr( object.__class__, column.name, marker )
            if value is marker or value is None:
                raise zope.app.keyreference.interfaces.NotYet( object )
            values.append( value )
    return tuple( values )

class AlchemistKeyReference( object ):

    zope.interface.implements(  zope.app.keyreference.interfaces.IKeyReference )

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
        session = get_session()
        query = session.query( klass )
        return query.get( self.primary_key )

    def __hash__( self ):
        return hash( (self.klass, self.primary_key ) )

    def __cmp__( self, other ):
        if self.key_type_id == other.key:
            return cmp( ( self.klass, self.primary_key ),
                        ( other.klass, other.primary_key ) )
        return cmp( self.key_type_id, other.key_type_id )
