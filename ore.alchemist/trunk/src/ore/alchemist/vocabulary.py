##############################################################################
#
# Copyright (c) 2008 Kapil Thangavelu <kapil.foss@gmail.com>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

"""

$Id$
"""

from ore.alchemist import Session
from zope import interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema import vocabulary

import sqlalchemy as rdb

class DatabaseSource( object ):
    """
    a simple implementation of vocabularies on top of a domain model, ideally should
    only be used with small skinny tables, actual value stored is the id
    """
    interface.implements( IContextSourceBinder )
    
    def __init__( self, domain_model, token_field, value_field, title_field=None, title_getter=None, order_by=None ):
        self.domain_model = domain_model
        self.token_field = token_field
        self.value_field = value_field
        self.title_field = title_field
        self.title_getter = title_getter
        self.order_by = order_by
        
    def constructQuery( self, context ):
        session = Session()
        query = session.query( self.domain_model )
        if self.order_by:
            query = query.order_by( self.order_by )
        return query
        
    def __call__( self, context=None ):
        query = self.constructQuery( context )
        results = query.all()
        
        terms = []
        title_field = self.title_field or self.token_field
        title_getter = self.title_getter or (lambda ob: getattr(ob, title_field))
        for ob in results:
            terms.append( 
                vocabulary.SimpleTerm( 
                    value = getattr( ob, self.value_field), 
                    token = getattr( ob, self.token_field),
                    title = title_getter(ob),
                    ))
                    
        return vocabulary.SimpleVocabulary( terms )

class ObjectSource( DatabaseSource ):
    """
    a vocabulary source, where objects are the values, for suitable for o2m fields.
    """
    
    def constructQuery( self, context ):
        session = Session()
        query = session.query( self.domain_model )
        return query        

class VocabularyTable( object ):
    """
    a database source implementation which caches values for the lifetime of the app, useful
    if the vocabulary definition is static.
    """
    
    _vocabulary = None
    
    def __init__( self, table, token_field, value_field ):
        self.table = table
        self.token_field = token_field
        self.value_field = value_field
        
    @property
    def vocabulary( self ):
        if self._vocabulary:
            return self._vocabulary
        terms = rdb.select( [ self.table.c[self.value_field], 
                          self.table.c[self.token_field] ] ).execute().fetchall()
        self._vocabulary = vocabulary.SimpleVocabulary.fromItems( terms )
        return self._vocabulary
        
    def __getattr__( self, name ):
        return getattr( self.vocabulary, name )
    
    def __call__( self, *args, **kw):
        return self.vocabulary
