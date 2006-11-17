"""
$Id$
"""


class PersonContainerView( object ):
    """ view for container
    """
    def __init__(self, context, request):
        self.context, self.request = context, request

    def search( self ):
        domain_class = self.context.domain_model
        d = {}
        for name in domain_class.c.keys():
            v = self.request.form.get(name)
            if v:
                d[name] = v
        if not d:
            return []
        return self.context.query(**d)
