#
import inspect, os
from alchemist.ui import container
from zope.app.pagetemplate import ViewPageTemplateFile

template_dir = os.path.join( os.path.dirname( inspect.getabsfile( container ) ), 'templates')

class ContainerListing( container.ContainerListing ):

    index = ViewPageTemplateFile( os.path.join( template_dir, 'generic-container.pt') )
    
    def listing( self ):
        formatter = self.formatter
        formatter.cssClasses['table'] = 'data'
        return formatter()
