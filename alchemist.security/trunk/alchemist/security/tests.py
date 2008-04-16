import unittest, transaction
from zope.testing import doctest, doctestunit
from zope.securitypolicy.interfaces import Allow, Deny, Unset
from ore.alchemist import Session
from sqlalchemy import orm
import sqlalchemy as rdb

def setUp( test ):
    pass
    
def tearDown( test ):
    pass

def test_suite():
    doctests = ('role.txt',)

    globs = dict(Session=Session, 
                 Allow=Allow,
                 Deny=Deny,
                 rdb=rdb,
                 transaction=transaction,
                 orm=orm)
    
    return unittest.TestSuite((
        doctestunit.DocFileSuite(filename,
                                 setUp = setUp,
                                 tearDown = tearDown,
                                 globs = globs,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS
                                 ) for filename in doctests
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')