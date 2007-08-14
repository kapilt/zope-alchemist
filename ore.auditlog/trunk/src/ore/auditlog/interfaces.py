#!/usr/bin/env python
# encoding: utf-8
"""
interfaces.py

Created by Kapil Thangavelu on 2007-08-10.
Copyright (c) 2007 __MyCompanyName__. All rights reserved.
"""

from zope import interface, schema

class IAuditLog( interface.Interface ):
    
    def __iter__( ):
        """ iterate through records of the audit log for this object in reverse 
            chronlogical order """
            
    def batch( start=0, size=20 ):
        """ return an iterator through the selected number of records in the audit log """
        
    def __len__( ):
        """ number of records in the audit log"""
        
class IAuditRecord( interface.Interface ):
    
    user_id = schema.TextLine( title=u"User Id" )        
    change_kind = schema.TextLine( title=u"Change Kind")        
    change_date = schema.TextLine( title=u"Change Date")
    content_uid = schema.TextLine( title=u"Content UID")
    content_type = schema.TextLine( title=u"Content Type")

    title = schema.TextLine( title=u"Title")
    description = schema.TextLine( title=u"Description")
    
