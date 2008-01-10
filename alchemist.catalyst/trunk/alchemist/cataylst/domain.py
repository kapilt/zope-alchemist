from sqlalchemy import orm
from ore.alchemist.model import ModelDescriptor
from ore.alchemist import sa2zs, interfaces
from zope import interface

def GenerateMapperInterface( domain_model,
                             interface_module,
                             interface_name=None,
                             bases=() ):

    # interface for domain model
    domain_interface_name = "I%s"%(domain_model.__name__)
    domain_mapper = orm.class_mapper( domain_model )
    domain_annotation = getattr( content, domain_model.__name__ + "Annotation", None)
    if domain_annotation is not None:
        domain_annotation = domain_annotation()
    
    domain_interface = sa2zs.transmute( domain_mapper.select_table,
                                        annotation=domain_annotation,
                                        interface_name = domain_interface_name,
                                        __module__ = interfaces.__name__,
                                        bases=(interfaces.IAlchemistContent,)
                                        )

    interface.classImplements( domain_model, domain_interface )
    setattr( interface_module, domain_interface_name, domain_interface )    
    
