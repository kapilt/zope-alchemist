"""
$Id: $
"""

from zope import interface, schema
from zope.component.interfaces import IObjectEvent

class ICatalystContext( interface.Interface ):
    
    domain_model = interface.Attribute("domain_model")
    
    domain_interface = interface.Attribute('domain_interface')
    
    echo = schema.Bool(title=u"Whether or not generated actions should be printed")
    
    
class ICatalystGeneration( IObjectEvent ):
    
    context = schema.Object( ICatalystContext )