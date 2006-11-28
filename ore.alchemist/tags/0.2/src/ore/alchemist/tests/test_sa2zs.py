
from unittest import TestSuite, makeSuite, TestCase, main
from datetime import datetime

from ore.alchemist.sa2zs import transmute
from zope import schema

import sqlalchemy as rdb

class SQLAlchemy2ZopeSchemaTests( TestCase ):

    def testSA2ZS( self ):

        metadata = rdb.DynamicMetaData("principals")
        
        users = rdb.Table('users', metadata,
                          rdb.Column('user_id',
                                     rdb.Integer,
                                     rdb.Sequence('user_id_seq', optional=True),
                                     primary_key = True),
                          rdb.Column('user_name', rdb.String(40), default=u'hello world' )
                      )

        iusers = transmute( users )
        self.assertEqual( tuple(schema.getFieldNamesInOrder( iusers )),
                          ('user_id', 'user_name') )

        fields = dict( schema.getFieldsInOrder(iusers) )
        # assert types and constraints
        self.assertTrue( isinstance(fields['user_id'], schema.Int ) )
        self.assertTrue( fields['user_id'].required )
        self.assertTrue( isinstance(fields['user_name'], schema.TextLine ) )
        self.assertEqual( fields['user_name'].max_length, 40 )
        self.assertEqual( fields['user_name'].default, u'hello world')

if __name__ == '__main__':
    main()
        
                                
        
        

        
    
        
