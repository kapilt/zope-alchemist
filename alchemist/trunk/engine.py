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
SQLAlchemy Zope Transaction Integration, this module provides an alternative
creation and lookup mechanism for SA engines, such that they are properly
integrated with zope transaction management and cached.

by default all engines in zope make use of thread local pools, Use of unique
connections is currently allowed, but discouraged.

the get_engine function is the primary accessor, it caches engines in order
to return existing engines when possible for the same dburi.


TODO
---
  post 0.2 refactoring, currently zope transactions aren't utilized to the transaction
  commits??

$Id$
"""

import sqlalchemy
import transaction

# install thread local module
import sqlalchemy.mods.threadlocal

from sqlalchemy import objectstore, create_engine as EngineFactory
from manager import AlchemyDataManager

def create_engine(*args, **kwargs):
    kwargs['strategy'] = 'zope'
    engine = EngineFactory( *args, **kwargs )
    name_or_url = args[0]
    _engines[ name_or_url ] = engine

_engines = {}
_engines_factories = {}

def get_engine_factory( name ):
    return _engines_factories[name]

def register_engine_factory( name, factory ):
    _engines_factories[ name ] = factory

def get_engine( dburi, **kwargs ):
    engine =  _engines.get( dburi )
    if engine is None:
        engine = create_engine( dburi, **kwargs )
    return engine

def list_engines( ):
    return _engine.keys()

