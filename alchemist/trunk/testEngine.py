"""
$Id$
"""

from unittest import TestCase, main

from sqlalchemy import objectstore
from engine import create_engine
import sqlalchemy as rdb
import transaction

class TestZopeEngine( TestCase ):


    def testObjectStoreCommit(self):
        # test that zope is driving the transaction.
        # autoload a table, create a mapper, create some instances
        # commit the objecstore, assert instance visibility,
        # abort zope transaction, assert instance destruction

        print "creating engine"
        engine = create_engine( 'zpgsql://database=baz', echo=True)

        print "creating table"
        ftable = rdb.Table("foobar", engine, autoload=True)
        
        class Foobar( object ):
            
            def __init__( self, xel=None, baz="abc"):
                self.xel = xel
                self.baz = baz

        print "assigning mapper"
        rdb.assign_mapper( Foobar, ftable)

        print "creating instance"
        a = Foobar(1)
        print "creating instance"        
        b = Foobar(2)

        print "committing objectstore"
        objectstore.commit()

        result = engine.execute('select * from foobar' )

        self.assertEqual( result.rowcount, 2)
        transaction.get().abort()

        result = engine.execute('select * from foobar' )
        self.assertEqual( result.rowcount, 0)        
        
        import time
        time.sleep(2)

    
if __name__ == '__main__':
    main()

    
