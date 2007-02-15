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

from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem

from zope.dottedname.resolve import resolve
from zope.interface import implements

from sqlalchemy.orm.query import Query
from sqlalchemy import objectstore

from ore.alchemist import named
from ore.alchemist.interfaces import IAlchemistContainer


class AlchemistContainer( SimpleItem ):

    implements( IAlchemistContainer )

    def __init__(self, id, domain_class, title=''):

        if isinstance( domain_class, type ):
            domain_class = named( domain_class )
        else:
            assert isinstance( domain_class, str)
            
        self.domain_class = domain_class
        self.id = id
        self.title = title
        
    def getDomainClass( self ):
        return resolve( self.domain_class )

    domain_model = property( getDomainClass )
    
    def add( self, *args, **kw):
        return self.domain_model( *args, **kw )

    def get( self, identity, **kwargs):
        return objectstore.get( self.domain_model, identity, **kwargs )
    
    def remove( self, object ):
        assert isinstance( object, self.domain_model )
        objectstore.delete( object )

    def values(self, offset=0, limit=20):
        query = objectstore.query( self.domain_model )
        return [res.__of__(self) for res in query.select()]

    def query(self, **kw ):
        query = objectstore.query( self.domain_model )
        return [ res.__of__(self) for res in query.select_by( **kw )]

    def __len__(self):
        return Query( self.domain_model ).count()

InitializeClass(AlchemistContainer)    
