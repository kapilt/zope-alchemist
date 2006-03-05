"""
$Id$
"""

from unittest import TestCase, main

class TestZopeEngine( TestCase ):


    def testObjectStoreCommit(self):
        engine = create_engine( 'zpgsql://database=baz', echo=True)
        
        import sqlalchemy as rdb
        
        ftable = rdb.Table("foobar", engine, autoload=True)
        
        class Foobar( object ):
            
            def __init__( self, xel=None, baz=False):
                self.xel = xel
                self.baz = baz
        
        rdb.assign_mapper( Foobar, ftable )
        print repr(ftable)

        a = Foobar(1)
        b = Foobar(2)

        #engine.reflecttable( table )
        #print repr(table)

        objectstore.commit()

        import time
        time.sleep(2)

    
if __name__ == '__main__':
    main()

    
