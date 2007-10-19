from zope.interface import Interface
from unittest import TestSuite, makeSuite, TestCase, main
from datetime import datetime

from ore.alchemist.zs2sa import transmute
from zope import schema

import sqlalchemy as rdb
from ore.alchemist.engine import get_engine

class ITestInterface( Interface ):
    
    ASCII = schema.ASCII(title=u'ASCII')
    ASCIILine = schema.ASCIILine(title=u'ASCIILine')
    Bool = schema.Bool(title=u'Bool')


class ZopeSchemaTransformTests( TestCase ):

    def testZS2SA( self ):

        meta = rdb.MetaData
        table = transmute(ITestInterface, meta)
        meta.create_all()

        self.assertEqual(table.columns.ASCII.type.__class__, rdb.TEXT)
        self.assertEqual(table.columns.ASCIILine.type.__class__, rdb.TEXT)
        self.assertEqual(table.columns.Bool.type.__class__, rdb.BOOLEAN)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite=TestSuite()
    suite.addTest(makeSuite(ZopeSchemaTransformTests))
    return suite


if __name__ == '__main__':
    main()
