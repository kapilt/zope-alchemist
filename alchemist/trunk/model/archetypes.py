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

from Products.alchemist.archetypes import ArchetypesSchemaModel as ModelBase
from sqlalchemy.util import OrderedDict


class ArchetypesSchemaModel( ModelBase ):

    def match( self, object ):
        return True

    def clear( self ):
        self._tables = OrderedDict()
        self._peer_factories = {}
        self.engine.tables = {}
        self.generateDefaults()

    def loadTypeByName(self, context, type_name):
        """
        load an archetype schema by name,
        for fk relationship callbacks
        """
        
