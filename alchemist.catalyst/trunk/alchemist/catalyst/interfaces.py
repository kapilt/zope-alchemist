"""
$Id: $
"""

from zope import interface, schema

class ICatalystContext( interface.Interface ):
    
    
    echo = schema.Bool(title=u"Whether or not generated actions should be printed")
    