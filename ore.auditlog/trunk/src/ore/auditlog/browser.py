"""
"""

from Products.Five.browser import BrowserView

import interfaces

class AuditLogView( BrowserView ):

    def __call__( self ):
        self.audit_log = interfaces.IAuditLog( self.context )
        return super(AuditLogView, self).__call__()



    
