"""

$Id: $

functionally this gives us class descriptors that return alchemsit z3 containers 

ideally we should hook into sa's property definition syntax, so we can have a z3 container
as an sa instructmented container class.
"""

from zope import interface
from zope.dottedname.resolve import resolve
from zope.app.security.protectclass import protectLikeUnto
from zope.security.proxy import removeSecurityProxy
from zope.location import ILocation
from ore.alchemist.container import PartialContainer
from sqlalchemy import orm

import interfaces

class _ManagedContainer( PartialContainer ):
    
    def __repr__( self ):
        m = self.__class__.__bases__[1]
        s = "%s.%s"%(m.__module__, m.__name__ )
        return "<Managed %s>"%s

    def __setitem__( self, key, value ):
        super( _ManagedContainer, self ).__setitem__( key, value )
        self.constraints.setConstrainedValues( self.__parent__, value )        
        
    def setConstraintManager( self, constraints ):
        self.constraints = constraints
        self.setQueryModifier( constraints.getQueryModifier( self.__parent__, self ) )

class ConstraintManager( object ):
    """
    manages the constraints on a managed container
    """
    
    def setConstrainedValues( self, instance, target ):
        """
        ensures existence of conformant constraint values
        to match the query.
        """
        
    def getQueryModifier( self, instance, container ):
        """
        given an instance inspect for the query to retrieve 
        related objects from the given alchemist container.
        """
        
class One2Many( ConstraintManager ):
    
    def __init__( self, fk):
        self.fk = fk
    
    def getQueryModifier( self, instance, container ):
        mapper = orm.class_mapper( instance.__class__ )
        primary_key = mapper.primary_key_from_instance( instance )[0]
        return container.domain_model.c[ self.fk ] == primary_key 
        
    def setConstrainedValues( self, instance, target ):
        trusted = removeSecurityProxy( instance )
        mapper = orm.object_mapper( trusted )
        primary_key = mapper.primary_key_from_instance( trusted )[0]
        column = target.__class__.c[ self.fk ]
        setattr( target, column.name, primary_key )
        
class Many2Many( ConstraintManager ):

    def __init__( self, join_fk ):
        pass

    def getQueryModifier( self, instance, container ):
        mapper = orm.object_mapper( instance )
        primary_key = mapper.primary_key_from_instance( instance )[0]
        
        #import pdb; pdb.set_trace()
        # user_group_membership.group_id = groups.group_id 
        # group
        #container.domain_model.c[ self.fk ] ==
        #sql.and_( 
        #            )
        return 
        
    def setConstrainedValues( self, instance, target ):
        mapper = orm.object_mapper( instance )        
        primary_key = mapper.primary_key_from_instance( instance )
        setattr( target, column.name, primary_key )

def one2many( name, container, fk ):
    constraint = One2Many( fk )
    container = ManagedContainerDescriptor( name, container, constraint )
    return container
    
class ManagedContainerDescriptor(object):
    
    _container_class = None
    
    interface.implements( interfaces.IManagedContainer )
    
    def __init__( self, name, container, constraint):
        self.name = name
        self.container  = container
        self.constraint = constraint
                
    def __get__( self, instance, class_):
        container = self.domain_container()
        if ILocation.providedBy( instance ):
            container.__parent__ = instance
            container.__name__ = self.name
        container.setConstraintManager( self.constraint )
        return container
    
    @property
    def domain_container( self ):
        if self._container_class:
           return self._container_class
        container_class= resolve( self.container )
        self._container_class = type( "ManagedContainer", ( _ManagedContainer, container_class), dict( container_class.__dict__) )        
        protectLikeUnto( self._container_class, container_class )
        return self._container_class

    
