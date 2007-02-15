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
integrated with zope transaction management.

by default all engines in zope make use of thread local pools, Use of unique
connections is currently allowed, but discouraged, 


so how does this all work..

 zope has a

 sqlalchemy has a couple of moving parts that play in its transaction story

  - engine

  - sql sessions
  
  - connection / pool

  - objecstore

 the sum of it is that sqlalchemy has an explicit begin/commit/rollback api
 on its engine, and does various gymanistics to make those reentrant and to
 allow for utilizing non transactional connection/object usage. none of which
 imo is particularly relevant in a zope context, where there is a transaction
 manager coordinating transactions between multiple transactional back ends.
 to that end, the integration starts by null implementing all the entry points
 into the sqlalchemy transaction machinery in an engine mixin class. Another
 mixin class provides zope transaction manager callback implementations that
 drive the sqlalchemy internals (objectstore/connection).

 on access via the get_engine api, we register an engine with the current transaction
 manager (TM), and the rest is taken care of for us.

 to enable sa and zope to both utilize the same access model for resources involved
 in a transaction, we setup engine pools to have their thread local option in effect.
 so now both sa is utilizing thread locals for resource management, and zope by default is
 also managing transactions in a thread local manner.


--- todo ---
savepoint integration requires further work in sqlalchemy uow, to snapshot
attributes.

update this integration to change from context to session usage when doing sa bookkeeping

$Id$
"""

import re

from zope.interface import implements

import sqlalchemy
from sqlalchemy.engine import SQLEngine, engine_descriptors
from sqlalchemy import objectstore, Table
from sqlalchemy.util import OrderedDict
from sqlalchemy import schema
from sqlalchemy.databases.information_schema import gen_tables
from sqlalchemy.databases.postgres import PGSQLEngine, PGSchemaGenerator as saPGSchemaGenerator



import transaction
from manager import AlchemyDataManager

def create_engine(uri, opts=None,**kwargs):
    """
    overriden create engine factory function from sqlalchemy.engine.create_engine

    we override to create non sqlalchemy contained engines, and to dynamically
    adapt engines to play nice with zope transactions.
    """
    m = re.match(r'(\w+)://(.*)', uri)
    if m is not None:
        (name, args) = m.group(1, 2)
        opts = {}
        def assign(m):
            opts[m.group(1)] = m.group(2)
        re.sub(r'([^&]+)=([^&]*)', assign, args)
        
    kwargs['use_threadlocal'] = True
    engine_factory = get_engine_factory( name )
    engine = engine_factory( opts, **kwargs)
    _engines[ uri ] = engine

    if not isinstance( engine, ZopeEngineMixin ):
        engine_class = type( "Zope%s"%engine.__class__.__name__, (ZopeEngineMixin, engine.__class__), {})
        new_engine = engine_class.__new__( engine_class )
        new_engine.__dict__.update( engine.__dict__ )
        del engine
        engine = new_engine
    return engine

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
    engine.do_zope_begin()
    return engine

def list_engines( ):
    return _engine.keys()

class SAFactory(object):
    def __init__(self, name):
        self.name = name
    def __call__(self, opts, **kw):
        module = getattr(__import__('sqlalchemy.databases.%s' % self.name).databases, self.name)
        return module.engine(opts, **kw)        

def register_defaults():
    for data in engine_descriptors():
        register_engine_factory( data['name'], SAFactory(data['name']) )

register_defaults()

SAVEPOINT_PREFIX = 'alchemy-'

class SANullTransactionMixin( object ):
    """
    null implement the builtin sql alchemy transaction interface, someone else
    is driving.
    """
    def begin(self):
        pass
    
    def rollback(self):
        pass

    def commit(self):
        pass

    def multi_transaction(self, tables, func):
        func()
        
    def transaction(self, func):
        func()

    def do_begin(self, connection):
        pass

    def do_rollback(self, connection):
        pass

    def do_commit(self, connection):
        pass


class ZopeEngineMixin( SANullTransactionMixin ):
    """
    a sqlalchemy engine mixin that participates in zope transactions, supports savepoints
    for databases implementing ansi savepoints.
    """

    def do_zope_begin( self ):
        if getattr(self.context, 'transaction', None) is None:
            conn = self.connection()
            self.do_begin(conn)
            self.context.transaction = conn

            manager = AlchemyDataManager( self )
            transaction.get().join( manager )

    def do_zope_rollback( self ):
        if self.context.transaction is None:
            return
        self.context.transaction.rollback()
        # not really nesc. sqlalchemy will do attr rollback
        # for clusters, it does need clearing though
        #objectstore.clear()

    def do_zope_rollback_savepoint( self, savepoint_name ):
        if self.context.transaction is None:
            raise RuntimeError("transaction not begun")

        if savepoint_name not in self.context.transaction.savepoints:
            raise RuntimeError("invalid savepoint %s"%savepoint_name)
        self.context.transaction.execute('rollback %s'%str(savepoint_name) )

    def do_zope_savepoint( self ):
        if self.context.transaction is None:
            return

        if self.context.savepoint is None:
            savepoint = 'alchemy-1'
            self.context.savepoints = []
        else:
            savepoint = 'alchemy-%d'%(len(self.context.savepoints))
        self.context.savepoints.append( savepoint )
        objectstore.commit()
        self.context.transaction.execute('SAVEPOINT %s'%savepoint )
        return savepoint

    def do_zope_work( self ):
        if self.context.transaction is None:
            return
        objectstore.commit()

    def do_zope_commit( self ):
        if self.context.transaction is None:
            return
        self.context.transaction.commit()
        self.context.transaction = None


