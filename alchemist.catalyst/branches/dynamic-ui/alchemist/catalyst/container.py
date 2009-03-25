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

def GenerateContainer( ctx,
                       container_name=None,
                       container_iname=None,
                       base_interfaces=() ):
        """
        generate a zope3 container class for a domain model
        """

        # create container
        container_name = container_name or \
                         ctx.domain_model.__name__ + 'Container'
        
        # allow passing in dotted python path
        if isinstance( ctx.container_module, (str, unicode) ):
            ctx.container_module = resolve( ctx.container_module )
        
        # if not present use the domain class's module
        elif ctx.container_module is None:
            ctx.container_module = resolve( ctx.domain_model.__module__ )
        
        # sanity check we have a module for the container
        assert isinstance(ctx.container_module, types.ModuleType ), "Invalid Container"
        
        # logging variables
        msg = ( ctx.domain_model.__name__, 
                ctx.container_module.__name__, 
                container_name )
                
        
        # if we already have a container class, exit                
        if getattr( ctx.container_module, container_name, None ):
            if ctx.echo:
                ctx.logger.debug("%s: found container %s.%s, skipping"%msg )
            ctx.container_class = getattr( ctx.container_module, container_name )
            return
            
        if ctx.echo:
            ctx.logger.debug("%s: generated container %s.%s"%msg )
        
        # if we already have a container class, exit        
        container_class = type( container_name,
                                (AlchemistContainer,),
                                dict(_class=ctx.domain_model,
                                     __module__=ctx.container_module.__name__ )
                                )
        
        setattr( ctx.container_module, container_name, container_class)
        
        # save container class on catalyst context
        ctx.container_class = container_class
        
        # interface for container
        container_iname = container_iname or "I%s"%container_name
        
        # if the interface module is none, then use the nearest one to the domain class
        if ctx.interface_module is None:
            ispec = ctx.domain_model.__module__.rsplit('.',1)[0]+'.interfaces'
            ctx.interface_module = resolve( ispec )
        
        msg = ( ctx.domain_model.__name__,
                ctx.container_module.__name__,
                container_iname )
        
        # if we already have a container interface class, skip creation
        container_interface = getattr( ctx.interface_module, container_iname, None )
        if container_interface is not None:
            assert issubclass( container_interface, IAlchemistContainer )
            if ctx.echo:
                ctx.logger.debug("%s: skipping container interface %s.%s for"%msg )
        else:
            if ctx.echo:
                ctx.logger.debug("%s: generated container interface %s.%s"%msg )            
            # ensure that our base interfaces include alchemist container 
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
                                                  __module__ = ctx.interface_module.__name__
                                                  )
            # store container interface for catalyst
            ctx.container_interface = container_interface

            setattr( ctx.interface_module, container_iname, container_interface )

        # setup security
        for n,d in container_interface.namesAndDescriptions(1):
            protectName( container_class, n, "zope.Public")

        if not container_interface.implementedBy(container_class):
            interface.classImplements(container_class, container_interface)
            
        ctx.container_interface = container_interface
        
