"""
$Id: $

Author: Kapil Thangavelu
Decription: generate a zope3 container class for a domain model

Todo:

 - generate container preconditions

"""

import types

from ore.alchemist.interfaces import IAlchemistContainer
from ore.alchemist.container import AlchemistContainer
from zope import interface
from zope.interface.interface import InterfaceClass
from zope.dottedname.resolve import resolve

def ContainerFactory( domain_model,
                      container_module=None,
                      interface_module=None,
                      bases = (),
                      container_name=None,
                      container_iname=None,
                      base_interfaces=() ):
        """
        generate a zope3 container class for a domain model
        """
        # create container
        container_name = container_name or domain_model.__name__ + 'Container'
        
        # allow passing in dotted python path
        if isinstance( container_module, (str, unicode) ):
            container_module = resolve( container_module )
        
        # if not present use the domain class's module
        elif container_module is None:
            container_module = resolve( domain_model.__module__ )
        
        # sanity check we have a module for the container
        assert isinstance(container_module, types.ModuleType ), "Invalid Container"
        
        container_class = type( container_name,
                                (AlchemistContainer,),
                                dict(_class=domain_model) )
        setattr( container_module, container_name, container_class)
        
        # interface for container
        container_iname = container_iname or "I%s"%container_name
        
        if issubclass( bases, interface.Interface ):
            base_interfaces = [ bases ]
            
        bases = base_interfaces or ( IAlchemistContainer,)
        
        found = False
        for b in bases:
            found = issubclass( b, IAlchemistContainer )
            if found: break
            
        if not found:
            if issubclass( bases, interface.Interface ):
                bases = [ bases, IAlchemistContainer ] 
            if isinstance( bases, list):
                bases.append( IAlchemistContainer )
            else:
                raise SyntaxError("invalid bases %r"%base_interfaces )
        
        
        # create interface
        container_interface = InterfaceClass( container_iname,
                                              bases = bases,
                                              __module__ = interface_module.__name__
                                              )
        
        setattr( interface_module, container_iname, container_interface )
        interface.classImplements( container_class, container_interface )    
        
        
