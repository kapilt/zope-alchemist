"""
$Id:$

Author: Kapil Thangavelu
Description:
  Provide ZCML Driven usage of catalyst
 
  functional requirements 
  
   - all features must be optional  
   - ui view registration ( need way to )   
   - relation viewlet creation
   - container creation ( module input )
   
  # domain class driven
  <rdb:catalyst 
       class=".domain.MyFoobar"
       descriptor="." />
  
"""

import logging
from zope import interface, schema
from zope.configuration.fields import GlobalObject, GlobalInterface

from zope import component
from zope.app.component.metaconfigure import utility, PublicPermission

import container
import domain
import interfaces
import ui

class ICatalystDirective( interface.Interface ):
    """ Auto Generate Components for a domain model
    """
    class_ = GlobalObject( 
                        title = u'Domain Class',
                        description = u'SQLAlchemy Mapped Class',
                        required = True,
                        )
                           
    descriptor = GlobalObject( 
                            title = u'Domain Descriptor',
                            description= u"Domain Model Configuration",
                            required = True 
                            )
                               
    ui_module = GlobalObject( 
                            title=u"Module For Views",
                            description = u"Generated Views and viewlets will be placed here",
                            required = False 
                            )
    
    interface_module = GlobalObject( 
                            title=u"Module For Interfaces", 
                            description=u"Module for generated domain interface",
                            required=False
                            )
    
    container_module = GlobalObject( 
                            title=u"Module For Container",
                            description=u"Module for generated container class",
                            required=False
                            )
    
    container_permission = schema.Text(
                            title=u"Permission to Protect Container Access",
                            description=u"If not specified then no permissions are associated",
                            required=False
                            )
                            
    layer = GlobalInterface(
                            title=u"UI Layer",
                            description=u"UI Layer for registration",
                            required=False,
                            default=interface.Interface
                            )
                            
    
    echo = schema.Bool( title=u"Echo Generated Items", required=False)

class CatalystContext(object):
    """
    context object where we store our configuration settings and generated
    objects.
    """
    
logging_setup = False

def catalyst(_context, 
             class_, 
             descriptor, 
             view_module=None,
             interface_module=None,
             container_module=None,
             ui_module=None,
             echo=False ):
    
    ctx = CatalystContext()
    
    ctx.zcml = _context
    ctx.descriptor = descriptor
    ctx.domain_model = class_
    ctx.interface_module = interface_module
    #ctx.mapper = 
    ctx.container_module = container_module
    ctx.ui_module = ui_module
    ctx.echo = echo

    ctx.views = {} # keyed by view type (add|edit)
    ctx.relation_viewlets = {} # keyed by relation name 
    ctx.logger = logging.getLogger('alchemist.catalyst')
    
    global logging_setup
    
    if ctx.echo and not logging_setup:
        logging_setup = True
        logging.basicConfig()
 
        formatter = logging.Formatter( 'catalyst %(module)s -> %(message)s')
        console = logging.StreamHandler()
        console.setLevel( logging.DEBUG )
        console.setFormatter( formatter )
        ctx.logger.addHandler( console )
        ctx.logger.setLevel( logging.DEBUG )
        #console.propagate = False       
        ctx.logger.propagate = False  
    
    try:
        # create a domain interface if it doesn't already exist 
        # this also creates an adapter between the interface and desc.
        domain.GenerateDomainInterface( ctx )
        
        domain.ApplySecurity( ctx )
        
        # behavior.ApplyIndexing( )
        # behavior.ApplyWorkflows( )
        # behavior.ApplyVersioning( )
        
        # create a container class 
        container.GenerateContainer( ctx )
        
        # generate views
        ui.GenerateViews( ctx )
    except:
        import sys,traceback, pdb
        traceback.print_exc()
        pdb.post_mortem(sys.exc_info()[-1])
        raise

    




