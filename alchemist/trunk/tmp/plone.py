"""
$Id$
"""

from sqlachemy import get_session
import zconnection

class AlchemistStorageConnection( zconnection.AlchemistConnection ):

    meta_type = "Alchemist Storage Connection"




