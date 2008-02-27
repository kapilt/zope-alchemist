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


class SQLAlchemy2ZopeSchemaTests( TestCase ):

    def testZS2SA( self ):

        db = get_engine('mysql://root@localhost/alc2', echo=True )
        meta = rdb.BoundMetaData( db )
        table = transmute(ITestInterface, meta)
        meta.create_all()

        self.assertEqual(table.columns.ASCII.type.__class__, rdb.TEXT)
        self.assertEqual(table.columns.ASCIILine.type.__class__, rdb.TEXT)
        self.assertEqual(table.columns.Bool.type.__class__, rdb.BOOLEAN)


if __name__ == '__main__':
    main()
