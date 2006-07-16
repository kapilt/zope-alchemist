"""
$Id$
"""
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase

ZopeTestCase.installProduct("Alchemist")

from unittest import TestCase, main

from sqlalchemy import objectstore
from sqlalchemy import * # to hard to fight ;-)
import sqlalchemy as rdb


from Products.Alchemist.engine import create_engine
from Products.Alchemist.changeset import SchemaChangeSet

import transaction


engine = create_engine( 'zpgsql://database=alchemy', echo=True)

users = Table('users', engine,
              Column('user_id', Integer, Sequence('user_id_seq', optional=True), primary_key = True),
              Column('user_name', String(40)),
              )

addresses = Table('email_addresses', engine,
    Column('address_id', Integer, Sequence('address_id_seq', optional=True), primary_key = True),
    Column('user_id', Integer, ForeignKey(users.c.user_id)),
    Column('email_address', String(40)),
    
)

orders = Table('orders', engine,
    Column('order_id', Integer, Sequence('order_id_seq', optional=True), primary_key = True),
    Column('user_id', Integer, ForeignKey(users.c.user_id)),
    Column('description', String(50)),
    Column('isopen', Integer),
    
)

orderitems = Table('items', engine,
    Column('item_id', INT, Sequence('items_id_seq', optional=True), primary_key = True),
    Column('order_id', INT, ForeignKey("orders")),
    Column('item_name', VARCHAR(50)),
    
)



class TestEngineUtility( TestCase ):

    def setUp(self):
        transaction.begin() # just insures an abort before we begin

    def tearDown(self):
        transaction.get().abort()

    def testTableSorter( self ):
        tables = engine.sort_tables()
        table_names = [t.name for t in tables]
        self.assertEqual( table_names, ['users', 'orders', 'items', 'email_addresses'] )

    def testTableCreation(self):
        engine.create_tables()
        self.assertEqual( engine.has_table('items'), True )
        self.assertEqual( engine.has_table('email_addresses'), True )        
        engine.create_tables()
        self.assertEqual( engine.has_table('items'), True )        

    def testTableDeletion(self):
        #self.assertEqual( engine.has_table('items'), False )
        engine.create_tables()
        self.assertEqual( engine.has_table('items'), True )        
        engine.drop_tables()
        self.assertEqual( engine.has_table('items'), False )
        self.assertEqual( engine.has_table('email_addresses'), False )                
        engine.drop_tables()
        self.assertEqual( engine.has_table('items'), False )                

    def XtestObjectStoreCommit(self):
        # test that zope is driving the transaction.
        # autoload a table, create a mapper, create some instances
        # commit the objecstore, assert instance visibility,
        # abort zope transaction, assert instance destruction

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

    
