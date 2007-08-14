#!/usr/bin/env python
# encoding: utf-8
"""
auditlog.py

Created by Kapil Thangavelu on 2007-08-10.
Copyright (c) 2007 ObjectRealms, LLC. All rights reserved.
"""

from ore.alchemist.manager import get_session
from ore.alchemist.zs2sa import transmute
from ore.alchemist.metadata import ZopeBoundMetaData
from sqlalchemy import mapper

import transaction
from zope import interface, component, schema

from AccessControl import getSecurityManager
from datetime import datetime

import interfaces, db

#################################
# Database
#################################

rdb_schema = ZopeBoundMetaData( db.database )

audit_table = transmute( interfaces.IAuditRecord, rdb_schema )

# create tables if they don't already exist
rdb_schema.create_all( checkfirst=True)

# commit a transaction to finalize table creation... needed?
transaction.commit()

#################################
# Audit Records
#################################

class AuditRecord( object ):
    
    interface.implements( interfaces.IAuditRecord )

    def __init__( self, **kw ):
        for field_name in schema.getFields( interfaces.IAuditRecord ):
            if not field_name in kw:
                print 'not found', field_name
                continue
            setattr( self, field_name, kw[ field_name ] )
                
#################################
# Audit Record Mapping
#################################

audit_mapping = mapper( AuditRecord, audit_table )

#################################
# 
    
#################################
# Audit Log
#################################

class AuditLog( object ):

    interface.implements( interfaces.IAuditLog )
    
    def __init__( self, context ):
        self.context = context

    def __iter__( self ):
        session = get_session()
        query = session.query( AuditRecord )
        return iter( query.select_by_content_uid( self.context.UID() ) )

    def __len__( self ):
        session = get_session()
        query = session.query( AuditRecord )
        return len( query.select_by_content_uid( self.context.UID() ) )      

    def createRecord( self, change_kind):
        record = AuditRecord( content_uid = self.context.UID(),
                              user_id = getSecurityManager().getUser().getId(),
                              change_kind = change_kind,
                              content_type = self.context.getPortalTypeName(),
                              change_date = datetime.now(),                          
                              **extractFields( self.context )
                              )
#################################
# Event Handlers
#################################

def handleAdd( ob, event ):
    log = interfaces.IAuditLog( ob )
    log.createRecord( change_kind='added' )
                 
def handleModified( ob, event ):
    log = interfaces.IAuditLog( ob )
    log.createRecord( change_kind='modified' )

def handleDeleted( ob, event ):
    log = interfaces.IAuditLog( ob )
    log.createRecord( change_kind='deleted' )

#################################
# Utilities
#################################

def extractFields( ob ):
    d = {}
    for i in ob.Schema().fields():
        d[ i.__name__ ] = i.getAccessor( ob )()
    return d
