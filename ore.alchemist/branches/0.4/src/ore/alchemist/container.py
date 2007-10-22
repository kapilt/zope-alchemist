"""

namechooser and contained implementation from z3c.zalchemy (ZPL 2.1)

$Id$
"""

from zope import interface

from zope.configuration.name import resolve
from zope.exceptions.interfaces import UserError
from zope.location.interfaces import ILocation
from zope.proxy import sameProxiedObjects
from zope.security.proxy import removeSecurityProxy

from zope.app.container.contained import Contained, ContainedProxy, NameChooser
from zope.app.container.interfaces import IContained

from persistent import Persistent
from sqlalchemy import orm, exceptions

from ore.alchemist import Session, interfaces

def stringKey( instance ):
    mapper = orm.object_mapper( instance )
    primary_key = mapper.primary_key_from_instance( instance )
    identity_key = '-'.join( map( str, primary_key ) )
    return identity_key

def valueKey( identity_key ):
    return identity_key.split('-')

def contained(obj, parent=None, name=None):
    """An implementation of zope.app.container.contained.contained
    that doesn't generate events, for internal use.

    Borrowed from SQLOS / z3c.zalchemy
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

        unproxied = removeSecurityProxy(self.context)
        if not name.startswith(unproxied._class.__name__+'-'):
            raise UserError("Invalid name for SQLAlchemy object")
        return True

    def chooseName(self, name, obj):
        # flush the object to make sure it contains an id
        session = Session()
        session.save(obj)
        return self.context._toStringIdentifier(obj)



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

    def batch(self, order_by=(), offset=0, limit=20):
        """
        this method pulls a subset/batch of values for paging through a container.
        """
        query = Session().query( self._class ).limit( limit ).offset( offset )
        if order_by:
            query = query.order_by( order_by )
        return [res.__of__(self) for res in query]
    
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
        session = Session()
        query = session.query( self._class )
        for obj in query:
            name = stringKey( obj )
            yield (name, contained(obj, self, name) )

    def get( self, name, default=None ):
        assert isinstance( name, basestring), "Invalid Key %r"%(name) 
        session = Session()
        value = session.query( self._class ).get( *valueKey( name ) )
        if value is None:
            return default
        return contained( value, self, name )

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
        session = Session()
        try:
            return session.query( self._class ).count()
        except exceptions.SQLError:
            return 0

## class PartialContainer( AlchemistContainer ):
##     """
##     an alchemist container that matches against an arbitrary subset, via definition
##     of a query. contents added to this container, may there fore not nesc. be accessible
##     from it, unless they also match the query.
##     """
    
##     _query = None

##     def setQuery( self, query ):
##         self._query = query

##     def getQuery( self ):
##         return self._query

##     subset_query = property( setQuery, getQuery )
        
        
