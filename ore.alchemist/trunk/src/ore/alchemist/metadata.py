"""
Variation on sqlalchemy metadata, which automatically registers engine with zope transaction
on usage.

$Id$
"""

from sqlalchemy import BoundMetaData, DynamicMetaData
from manager import register


class ZopeBoundMetaData( BoundMetaData ):
    """ Metadata which automatically registers engine with zope transaction on usage
    """
    def _get_engine( self ):
        engine = super( ZopeBoundMetaData, self )._get_engine()
        register( engine )
        return engine
    

    
