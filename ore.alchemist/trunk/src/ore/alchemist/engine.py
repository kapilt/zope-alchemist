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

this module provides an alternative creation and lookup mechanism for SA
engines, such that they are properly integrated with zope transaction
management, cached by dburi, and use a zope compatible strategy.

the get_engine function is the primary accessor, it caches engines in order
to return existing engines when possible for the same dburi.

also provides a zope vocabulary utility for enumerating engine urls

$Id$
"""

import sqlalchemy
import transaction

# install thread local module
import sqlalchemy.mods.threadlocal
import strategy

from sqlalchemy import objectstore, create_engine as EngineFactory

from zope.interface import implements
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary

from interfaces import IEngineVocabularyUtility
from manager import register

__all__ = [ 'create_engine', 'get_engine', 'list_engines' ]

_engines = {}

def create_engine(*args, **kwargs):
    kwargs['strategy'] = 'zope'
    engine = EngineFactory( *args, **kwargs )
    name_or_url = args[0]
    _engines[ name_or_url ] = engine
    register( engine )
    return engine

def get_engine( dburi, **kwargs ):
    engine =  _engines.get( dburi )
    if engine is None:
        engine = create_engine( dburi, **kwargs )
    register( engine )
    return engine

def list_engines( ):
    return _engine.keys()

def iter_engines():
    return _engines.itervalues()



class EngineUtility( object ):
    implements( IEngineVocabularyUtility )
    engines = property( list_engines )
    
def EngineVocabulary( context ):
    utility = getUtility( IEngineVocabularyUtility )
    return SimpleVocabulary.fromValues( utility.engines )


    
