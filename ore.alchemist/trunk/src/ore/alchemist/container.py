##############################################################################
#
# Copyright (c) Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
portions from zope3 community (z3c.zalchemy) namechooser and contained
implementation from z3c.zalchemy (ZPL 2.1).


$Id$
"""

from zope import interface

from zope.configuration.name import resolve
from zope.exceptions.interfaces import UserError
from zope.location.interfaces import ILocation
from zope.proxy import sameProxiedObjects

from zope.app.container.contained import Contained, ContainedProxy, NameChooser
from zope.app.container.interfaces import IContained

from persistent import Persistent
from sqlalchemy import orm, exceptions

from ore.alchemist import Session, interfaces

def stringKey( instance ):
    mapper = orm.object_mapper( instance )
    primary_key = mapper.primary_key_from_instance( instance )
    identity_key = '-'.join( map( str, primary_key ) )
    return "obj-%s"%identity_key

def valueKey( identity_key ):
    if not isinstance( identity_key, (str, unicode)):
        return identity_key
    if identity_key.startswith('obj-'):
        return identity_key.split('-')[1:]
    raise KeyError

def contained(obj, parent=None, name=None):
    """An implementation of zope.app.container.contained.contained
    that doesn't generate events, for internal use.

    copied from SQLOS / z3c.zalchemy
    """
    if (parent is None):
        raise TypeError('Must provide a parent')

    if not IContained.providedBy(obj):
        if ILocation.providedBy(obj):
            interface.directlyProvides(obj, IContained,
                                       interface.directlyProvidedBy(obj))
        else:
            obj = ContainedProxy(obj)

    oldparent = obj.__parent__
    oldname = obj.__name__

    if (oldparent is None) or not (oldparent is parent
                                   or sameProxiedObjects(oldparent, parent)):
        obj.__parent__ = parent

    if oldname != name and name is not None:
        obj.__name__ = name

    return obj

class SQLAlchemyNameChooser(NameChooser):
    # from z3c.zalchemy
    
    def checkName(self, name, content):
        if isinstance(name, str):
            name = unicode(name)
        elif not isinstance(name, unicode):
            raise TypeError("Invalid name type", type(name))
        if u'-' in name: # valueKey()
            return True
        raise UserError("Invalid name for SQLAlchemy object")
        
    def chooseName(self, name, obj):
        # flush the object to make sure it contains an id
        session = Session()
        session.save(obj)
        return stringKey(obj)

class ContainerSublocations( object ):
    """
    by default, we do not dispatch to containers, as we can contain arbitrarily large sets
    """ 

    def __init__(self, container):
        self.container = container

    def sublocations(self):
        return ()


class AlchemistContainer( Persistent, Contained ):
    """ a persistent container with contents from an rdbms
    """

    _class_name = ""
    _class = None
    
    interface.implements( interfaces.IAlchemistContainer )

    def setClassName( self, name ):
        self._class_name = name
        self._class = resolve( name )

    def getClassName( self ):
        return self._class_name

    class_name = property( getClassName, setClassName )

    @property
    def domain_model( self ):
        return self._class

    def batch(self, order_by=(), offset=0, limit=20, filter=None):
        """
        this method pulls a subset/batch of values for paging through a container.
        """
        query = self._query.limit( limit ).offset( offset )
        if filter:
            query = query.filter( filter )
        if order_by:
            query = query.order_by( order_by )
        for ob in query:
            ob = contained( ob, self, stringKey(ob) )
            yield ob

    def query( self, **kw):
        return list( self._query.filter_by( **kw ) )

    @property
    def _query( self ):
        session = Session()
        query = session.query( self._class )
        return query
        
    #################################
    # Container Interface
    #################################
    
    def keys( self ):
        for name, obj in self.items():
            yield name

    def values( self ):
        for name, obj in self.items():
            yield obj

    def items( self ):
        for obj in self._query:
            name = stringKey( obj )
            yield (name, contained(obj, self, name) )

    def get( self, name, default=None ):
        try:
            key = valueKey( name )
        except KeyError:
            return default
        value = self._query.get( key )
        if value is None:
            return default
        value = contained( value, self, stringKey(value) )
        return value

    def __iter__( self ):
        return iter( self.keys() )

    def __getitem__( self, name ):
        value = self.get( name )
        if value is None:
            raise KeyError( name )
        return value

    def __setitem__( self, name, item ):
        session = Session()
        session.save( item )
        
    def __delitem__( self, name ):
        instance = self[ name ]
        session = Session()
        session.delete( instance )
    
    def __contains__( self, name ):
        return self.get( name ) is not None

    def __len__( self ):
        try:
            return self._query.count()
        except exceptions.SQLError:
            return 0

class PartialContainer( AlchemistContainer ):
    """
    an alchemist container that matches against an arbitrary subset, via definition
    of a query modification function. contents added to this container, may there 
    fore not nesc. be accessible from it, unless they also match the query. the
    alchemist ui views provide add views which can maintain the constraint
    """
    
    _subset_query = None
     
    def setQueryModifier( self, query ):
        self._subset_query = query
         
    def getQueryModifier( self ):
        return self._subset_query
    
    subset_query = property( setQueryModifier, getQueryModifier )
    
    @property
    def _query( self ):
        query = super( PartialContainer, self)._query 
        return query.filter( self._subset_query )
