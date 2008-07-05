import unittest
import re

from zope.testing import doctest, renormalizing
from zope.app.testing import placelesssetup


def setUp( test ):
    placelesssetup.setUp()

def tearDown( test ):
    placelesssetup.tearDown
    
def test_suite():
    #import testing
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'readme.txt',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            )))
