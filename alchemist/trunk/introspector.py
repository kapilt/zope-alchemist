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
$Id$
"""

from OFS.SimpleItem import SimpleItem
from zope.interface import implements
from interfaces import IAlchemistIntrospector

class AlchemistIntrospector( SimpleItem ):

    implements( IAlchemistIntrospector )

    def __init__( self, id, title, engine_uri, schema=None ):
        self.id = id
        self.title = title
        self.engine_uri = engine_uri
        self.schema = schema

    def _introspector( self ):

        if self._v_introspector:
            return self._v_introspector

        self._v_introspector = SchemaIntrospector()
        self._v_introspector.bindEngine( engine_uri, self.schema )

    introspector = property( _introspector )

