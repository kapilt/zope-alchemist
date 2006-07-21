"""
$Id$
"""

from Products.alchemist.container import AlchemistContainer

class ContainerAddingView:

    """Add view for alchemist container view.
    """

    def __call__(self, add_input_name='', domain_class='', title='', submit_add=''):
        
        if not submit_add or not domain_class:
            return self.index()

        obj = AlchemistContainer( add_input_name, domain_class, title  )
        self.context.add(obj)
        self.request.response.redirect(self.context.nextURL())
        return ''


