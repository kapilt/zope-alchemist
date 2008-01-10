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
  <rdb:bind 
       class=".domain.MyFoobar"
       descriptor="." />
  
"""

from zope import interface, schema
from zope.configuration.fields import GlobalObject

from zope import component
from zope.app.component.metaconfigure import utility, PublicPermission

import container
import interfaces

class ICatalystDirective( interface.Interface ):
    """ Auto Generate Components for a domain model
    """
    class_ = GlobalObject( title = u'Domain Class',
                           description = u'SQLAlchemy Database URL',
                           required = True,
                           )
                           
    descriptor = GlobalObject( title = u'Domain Descriptor',
                               description= u"Domain Model Configuration",
                               required = True )
                               
    view_module = GlobalObject( title=u"Module For Views",
                                description = u"Generated Views and viewlets will be placed here",
                                required = False )
    
    interface_module = GlobalObject( title=u"Module For Interfaces")
    
    container_module = GlobalObject( title=u"Module For Container")

    echo = schema.Bool( title=u"Echo Generated Items")
    
def cataylst(_context, class_, descriptor ):
    
    # create a container class 
    container.ContainerFactory( class_ )
    
    # create a domain interface if it doesn't already exist 
    # this also creates an adapter between the domain interface 
    # and the 
    




