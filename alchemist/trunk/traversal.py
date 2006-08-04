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

from zope.app.traversing.interfaces import ITraversable, TraversalError
from zope.component import ComponentLookupError
from zope.interface import implements 
from zExceptions import NotFound

from Products.Five.traversable import FiveTraversable

class ContainerTraversal( FiveTraversable ):

    implements( ITraversable )

    def __init__(self, context ):
        self._subject = context

    def traverse( self, name, furtherPath ):

        # first try to find a view
        try:
            next = super( ContainerTraversal, self).traverse( name, furtherPath )
            if next is not None:
                return next
        except (ComponentLookupError, AttributeError, KeyError, NotFound, TraversalError):
            pass

        # next try to load the domain record

        # ugh.. XXX temp hack convert to int
        try:
            oid = int( name )
        except: # bobo traverse gets called alot, skip for now if we don't have an int
            raise AttributeError ( name )
            
        object = self._subject.get( oid )

        if object is not None:
            return object.__of__( self._subject )
        
        raise TraversalError( name )
        
        
