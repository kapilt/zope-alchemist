"""
$Id$
"""

from Products.alchemist.container import AlchemistContainer

class ContainerAddingView:

    """Add view for demo content.
    """

    def __call__(self, container_id='', domain_class='', title='', submit_add=''):

        import pdb; pdb.set_trace()
        
        if not submit_add or not domain_class:
            return self.index()

        obj = AlchemistContainer( container_id, domain_class, title  )
        self.context.add(obj)
        self.request.response.redirect(self.context.nextURL())
        return ''

