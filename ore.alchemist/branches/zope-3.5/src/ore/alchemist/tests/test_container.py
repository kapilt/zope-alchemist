"""
$Id$
"""

import unittest
import doctest

from zope.app.testing import setup
from zope.testing.doctestunit import DocFileSuite


import sqlalchemy as rdb
from sqlalchemy import orm


from ore.alchemist import Session
import transaction
metadata = rdb.MetaData()

simple_content_table = rdb.Table(
    'simple_content',
    metadata,
    rdb.Column('id', rdb.Integer, primary_key = True ),
    rdb.Column('content', rdb.String )
    )

multikey_content_table = rdb.Table(
    'multikey_content',
    metadata,
    rdb.Column('id1', rdb.Integer, primary_key = True),
    rdb.Column('id2', rdb.String,  primary_key = True),
    )

class SimpleContent( object ):
    def __init__( self, text='simple'):
        self.text = text
class MultiKeyContent( object ):
    def __init__( self, id1=None, id2=None):
        if id1: self.id1 = id1
        if id2: self.id2 = id2

orm.mapper( SimpleContent, simple_content_table )
orm.mapper( MultiKeyContent, multikey_content_table )

def setUp( test ):
    setup.placefulSetUp()
    test._engine = rdb.create_engine('sqlite://')
    metadata.bind = test._engine
    metadata.create_all()
    
def tearDown( test ):
    del test._engine
    del metadata._bind
    setup.placefulTearDown()
    
def test_suite():
    return unittest.TestSuite((
        DocFileSuite('../container.txt',
                     setUp=setUp, tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')


