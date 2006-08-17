

class DomainRecord( object ):

    def __init__(self, **kw):
        for k,v in kw.iteritems():
            setattr( self, k, v )
                
