from sqlalchemy import orm
from ore.alchemist.model import ModelDescriptor
from ore.alchemist import sa2zs, interfaces
from zope import interface
from zope.dottedname.resolve import resolve

def GenerateDomainInterface( domain_model,
                             descriptor,
                             interface_module=None,
                             interface_name=None,
                             bases=() ):

    # when called from zcml, most likely we'll get a class not an instance
    # if it is a class go ahead and call instantiate it
    if isinstance( descriptor, type):
        descriptor = descriptor()
                             
    # if the interface module is none, then use the nearest one to the domain class
    if interface_module is None:
        ispec = domain_model.__module__.rsplit('.',1)[0]+'.interfaces'
        interface_module = resolve( ispec )

    # interface for domain model
    if not interface_name:
        interface_name = "I%s"%(domain_model.__name__)
        
    # use the class's mapper select table as input for the transformation
    domain_mapper = orm.class_mapper( domain_model )
    domain_interface = sa2zs.transmute( domain_mapper.select_table,
                                        annotation=descriptor,
                                        interface_name = interface_name,
                                        __module__ = interface_module.__name__,
                                        bases=(interfaces.IAlchemistContent,)
                                        )

    interface.classImplements( domain_model, domain_interface )
    setattr( interface_module, interface_name, domain_interface )    
    
