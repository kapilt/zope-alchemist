"""
$Id$
"""

import unittest
import doctest

from zope.app.testing import setup
from zope.testing.doctestunit import DocFileSuite


import sqlalchemy as rdb
from sqlalchemy import orm


from ore.alchemist import Session, container
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
    def __init__(self, content='v'):
        print 'sc init', content
        self.content = content 
class MultiKeyContent( object ): pass

orm.mapper( SimpleContent, simple_content_table )
orm.mapper( MultiKeyContent, multikey_content_table )

engine = rdb.create_engine('sqlite://memory', echo=True)
metadata.bind = engine
metadata.create_all()

transaction.abort()


session = Session()

a = SimpleContent()
session.save(a)

b = SimpleContent()
session.save(b)

d = SimpleContent()
session.save(d)

print 'joined', session.joined
transaction.commit()

print 'new session'
session = Session()
print 'oined', session.joined

act = container.AlchemistContainer()
act._class = SimpleContent

#print len(act)
#print list(act.items())
#import pdb; pdb.set_trace()
#ss = orm.class_mapper( SimpleContent )
#print ss.primary_key_argument
#print ss.pks_by_table.values()
#print ss.primary_key
#print 'a'


 
print 'before'
print len(act)
print 'new'
#act['1'] = 

d = SimpleContent('c')
print 'ce'
print len(act)
session.save(d)
print 'cd'
#import pdb; pdb.set_trace()
print len(act)


print 'new'
e = SimpleContent('d')
print 'ct'
print len(act)
session.save(e)
print 'ct'
print len(act)

print 'joined', session.joined
transaction.commit()
#transaction.abort()
print 'joined', session.joined

session = Session()
print len(act)

transaction.abort()

## def setUp( test ):
##     setup.placefulSetUp()
##     test._engine = rdb.create_engine('sqlite://memory', echo=True)
##     metadata.bind = test._engine
##     metadata.create_all()
     
## def tearDown( test ):
##     del test._engine
##     del metadata._bind
##     setup.placefulTearDown()
    
## def test_suite():
##     return unittest.TestSuite((
##         DocFileSuite('../container.txt',
##                      setUp=setUp, tearDown=tearDown,
##                      optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
##                      ),
##         ))

## if __name__ == '__main__':
##     unittest.main(defaultTest='test_suite')


