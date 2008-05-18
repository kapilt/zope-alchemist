
from alchemist.ui import relation
from zope.viewlet import manager

class ContentViewletManager( manager.ViewletManagerBase ):

    sort_order = [
        'alchemist.attributes.edit',
        'alchemist.attributes.view',        
        ]
    
    def sort( self, viewlets ):
        names = [ k for k,v in viewlets]
        viewlet_map = dict( viewlets )
        sorted_viewlets = [ (k,viewlet_map[k]) for k in self.sort_order if k in names ]
        for n in names:
            if n not in self.sort_order:
                sorted_viewlets.append( ( n, viewlet_map[n] ) )
        return sorted_viewlets

class Many2ManyDisplay( relation.Many2ManyDisplay ):

    def setUpFormatter( self ):
        formatter = super( Many2ManyDisplay, self).setUpFormatter()
        formatter.cssClasses['table'] = 'data'
        return formatter

class Many2ManyEdit( relation.Many2ManyEdit ):

    def setUpFormatter( self ):
        formatter = super( Many2ManyEdit, self).setUpFormatter()
        formatter.cssClasses['table'] = 'data'
        return formatter
