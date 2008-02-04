"""
$Id: $
"""

from zope import interface
from zope.dottedname.resolve import resolve
from zope.app.security.protectclass import protectLikeUnto
from zope.security.proxy import removeSecurityProxy

from ore.alchemist.container import PartialContainer
from sqlalchemy import orm

import interfaces

# alternatively hand turn a z3 container collection class for an object.

class _ManagedContainer( PartialContainer ):
    
    def __repr__( self ):
        m = self.__class__.__bases__[1]
        s = "%s.%s"%(m.__module__, m.__name__ )
        return "<Managed %s>"%s
        
class ManagedContainer(object):
    
    _container_class = None
    
    interface.implements( interfaces.IManagedContainer )
    
    def __init__( self, name, container, fk):
        self.name = name
        self.container = container
        self.fk = fk
                
    def __get__( self, instance, class_):
        container = self.domain_container()
        container.__parent__ = instance
        container.__name__ = self.name
        mapper = orm.object_mapper( instance )
        primary_key = mapper.primary_key_from_instance( instance )[0]
        container.setQueryModifier( container.domain_model.c[ self.fk ] == primary_key )
        return removeSecurityProxy( container )
    
    @property
    def domain_container( self ):
        if self._container_class:
           return self._container_class
        container_class= resolve( self.container )
        self._container_class = type( "ManagedContainer", ( _ManagedContainer, container_class), dict( container_class.__dict__) )        
        protectLikeUnto( self._container_class, container_class )
        return self._container_class
