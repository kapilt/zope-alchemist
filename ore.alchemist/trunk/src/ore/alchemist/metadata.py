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
Variation on sqlalchemy metadata, which automatically registers engine with zope transaction
on usage.

$Id$
"""

from sqlalchemy import BoundMetaData, DynamicMetaData
from manager import register


class ZopeBoundMetaData( BoundMetaData ):
    """ Metadata which automatically registers engine with zope transaction on usage
    """
    def _get_engine( self ):
        engine = super( ZopeBoundMetaData, self )._get_engine()
        register( engine )
        return engine
    

    
