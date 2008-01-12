from sqlalchemy import orm
from ore.alchemist.model import ModelDescriptor
from ore.alchemist import sa2zs, interfaces
from zope import interface
from zope.dottedname.resolve import resolve

def GenerateDomainInterface( ctx, interface_name=None ):

    # when called from zcml, most likely we'll get a class not an instance
    # if it is a class go ahead and call instantiate it
    if isinstance( ctx.descriptor, type):
        ctx.descriptor = ctx.descriptor()
                             
    # if the interface module is none, then use the nearest one to the domain class
    if ctx.interface_module is None:
        ispec = ctx.domain_model.__module__.rsplit('.',1)[0]+'.interfaces'
        ctx.interface_module = resolve( ispec )
    
    # interface for domain model
    if not interface_name:
        interface_name = "I%s"%( ctx.domain_model.__name__)
    
    msg = ( ctx.domain_model.__name__,
            ctx.interface_module.__name__,
            interface_name )
    
    if ctx.echo:
        ctx.logger.debug("%s: generated interface %s.%s"%msg )
                        
    # use the class's mapper select table as input for the transformation
    domain_mapper = orm.class_mapper( ctx.domain_model )
    domain_interface = sa2zs.transmute( domain_mapper.select_table,
                                        annotation=ctx.descriptor,
                                        interface_name = interface_name,
                                        __module__ = ctx.interface_module.__name__,
                                        bases=(interfaces.IAlchemistContent,)
                                        )

    interface.classImplements( ctx.domain_model, domain_interface )
    setattr( ctx.interface_module, interface_name, domain_interface )    
    
    ctx.domain_interface = domain_interface
    
