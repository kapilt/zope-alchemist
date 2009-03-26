from sqlalchemy import orm
#from ore.alchemist.model import ModelDescriptor
from ore.alchemist import sa2zs, interfaces
from alchemist.traversal.managed import ManagedContainerDescriptor
from zope import interface
from zope.dottedname.resolve import resolve
#from zope.location import ILocation
#from zope.app.container.interfaces import IContainer
from zope.app.security.protectclass import protectName, protectSetAttribute, protectLikeUnto

def ApplySecurity( ctx ):
    # setup security
    #
    for c in ctx.domain_model.__bases__:
        if c is object:
            continue
        protectLikeUnto( ctx.domain_model, c )

    attributes = set([n for n,d in \
                      ctx.domain_interface.namesAndDescriptions(1)])
    attributes = attributes.union(
        set( [ f.get('name') for f in ctx.descriptor.fields] )
        )

    descriptor = ctx.descriptor
    for n in attributes:
        model_field = descriptor.get(n)
        p = model_field and model_field.view_permission or 'zope.Public'
        protectName( ctx.domain_model, n, p )
    
    for n in attributes:
        model_field = descriptor.get(n)
        p = model_field and model_field.edit_permission or 'zope.Public' # 'zope.ManageContent'
        protectSetAttribute( ctx.domain_model, n, p)
        
    for k, v in ctx.domain_model.__dict__.items():
        if isinstance(v, ManagedContainerDescriptor) or isinstance(
            v, orm.attributes.InstrumentedAttribute):
            protectName( ctx.domain_model, k, "zope.Public" )

def getDomainInterfaces( domain_model ):
    """return the domain bases for an interface as well
    as a filtered implements only list """
    domain_bases = []
    domain_implements = []    
    for iface in interface.implementedBy( domain_model ):
        if interfaces.IIModelInterface.providedBy( iface ):
            domain_bases.append( iface )
        else:
            domain_implements.append( iface )
    domain_bases = tuple(domain_bases) or (interfaces.IAlchemistContent,)
    return (domain_bases, domain_implements)
    
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
    
    bases, implements = getDomainInterfaces( ctx.domain_model )
    
    # use the class's mapper select table as input for the transformation
    domain_mapper = orm.class_mapper( ctx.domain_model )
    # 0.4 and 0.5 compatibility, 0.5 has the table as local_table (select_table) is none lazy gen?
    domain_table  = getattr( domain_mapper, 'local_table', domain_mapper.select_table )
    domain_interface = sa2zs.transmute( domain_table,
                                        annotation=ctx.descriptor,
                                        interface_name = interface_name,
                                        __module__ = ctx.interface_module.__name__,
                                        bases=bases
                                        )

    implements.insert(0, domain_interface)

    # if we're replacing an existing interface, make sure the new
    # interface implements it
    old = getattr( ctx.interface_module, interface_name, None)
    if old is not None:
        implements.append(old)
    
    interface.classImplementsOnly( ctx.domain_model, *implements )
    setattr( ctx.interface_module, interface_name, domain_interface )    
    
    ctx.domain_interface = domain_interface
    
