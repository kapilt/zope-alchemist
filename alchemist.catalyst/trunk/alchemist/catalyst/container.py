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

# XXX should be removed
from zope.app.security.protectclass import protectName

def GenerateContainer( domain_model,
                      container_module=None,
                      interface_module=None,
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

        # if we already have a container class, exit
        if getattr( container_module, container_name, None ):
            return                

        container_class = type( container_name,
                                (AlchemistContainer,),
                                dict(_class=domain_model, __module__=container_module.__name__ )
                                )

        setattr( container_module, container_name, container_class)
            
        # interface for container
        container_iname = container_iname or "I%s"%container_name

        # if the interface module is none, then use the nearest one to the domain class
        if interface_module is None:
            ispec = domain_model.__module__.rsplit('.',1)[0]+'.interfaces'
            interface_module = resolve( ispec )

        # if we already have a container interface class, exit
        if getattr( interface_module, container_iname, None ):
            return
        
        if base_interfaces:
            assert isinstance( base_interfaces, tuple )
            found = False
            for bi in base_interfaces:
                found = issubclass( bi, IAlchemistContainer )
                if found: break
            if not found:
                base_interfaces = base_interfaces + ( IAlchemistContainer,)
        else:
            base_interfaces = ( IAlchemistContainer, )
        
        # create interface
        container_interface = InterfaceClass( container_iname,
                                              bases = base_interfaces,
                                              __module__ = interface_module.__name__
                                              )

        for n,d in container_interface.namesAndDescriptions(1):
            protectName( container_class, n, "zope.Public")
            
        setattr( interface_module, container_iname, container_interface )
        interface.classImplements( container_class, container_interface )    
        
        
