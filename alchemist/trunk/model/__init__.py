"""
$Id$
"""

import default

_models = []

def registerModel( model ):
    _models.append( model )


def getModelFor( object ):
    for m in _models:
        if m.match( object ):
            return m



registerModel( default.DefaultSchemaModel )

    
