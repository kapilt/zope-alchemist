
from unittest import TestSuite, makeSuite, TestCase, main

from zope import schema, interface
from ore.alchemist.zs2sa import transmute

import sqlalchemy as rdb

class ITestInterface( interface.Interface ):
    
    ASCII = schema.ASCII(title=u'ASCII')
    ASCIILine = schema.ASCIILine(title=u'ASCIILine')
    Bool = schema.Bool(title=u'Bool')


class ZopeSchemaTransformTests( TestCase ):

    def testZS2SA( self ):

        meta = rdb.MetaData()
        table = transmute(ITestInterface, meta)

        self.assertEqual(table.columns.ASCII.type.__class__, rdb.String)
        self.assertEqual(table.columns.ASCIILine.type.__class__, rdb.String)
        self.assertEqual(table.columns.Bool.type.__class__, rdb.BOOLEAN)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite=TestSuite()
    suite.addTest(makeSuite(ZopeSchemaTransformTests))
    return suite

