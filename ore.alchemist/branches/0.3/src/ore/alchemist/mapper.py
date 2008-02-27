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
a decorating mapper for sqlalchemy that utilizes field properties for attribute validation

-- pass on set and structs
-- currently has issues with fk references
"""

from bind import bindClass
from sqlalchemy import mapper

from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary
from zope import interface
import interfaces

class DomainVocabularyUtility( object ):
    
    interface.implements( interfaces.IDomainVocabularyUtility )

    def __init__( self ):
        self._domain_classes = []

    def add( self, klass ):
        self._domain_classes.append( "%s.%s"%(klass.__module__, klass.__name__ ) )

    def __iter__( self ):
        return iter( self._domain_classes )

    def __call__( self ):
        return self

DomainUtility = DomainVocabularyUtility()
    
def DomainVocabulary( context ):
    utility = getUtility( interfaces.IDomainVocabularyUtility )
    return SimpleVocabulary.fromValues( utility )

def bind_mapper( klass, *args, **kw):
    klass_mapper = mapper( klass, *args, **kw )
    bindClass( klass, klass_mapper )
    DomainUtility.add( klass )    
    return klass_mapper
