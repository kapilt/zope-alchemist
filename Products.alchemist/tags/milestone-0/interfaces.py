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
from zope.interface import Interface


class IAlchemySchemaModel( Interface ):

    def match( object ):
        """
        should this model be used for the given object
        """

    def clear( ):
        """
        clear all loaded state for the model
        """

    def __getitem__( key ):
        """
        return the peer factor for the given key or None
        """

    def loadType( archetype_klass, context ):
        """
        load the schema from the given archetype klass,
        translate it to an alchemy model, and alchemy
        mapped peer class, uses context as an acquisition
        context if nesc.
        """

    def loadInstance( instance ):
        """
        as above but load from an instance...

        does not support context based schemas.. need to
        qualify the name on storage.
        """
        
