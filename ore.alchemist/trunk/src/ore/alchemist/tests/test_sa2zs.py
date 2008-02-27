
from unittest import TestSuite, makeSuite, TestCase, main
from datetime import datetime

from ore.alchemist.sa2zs import transmute
from zope import schema, interface
from zope.app.container.constraints import containers
from zope.app.container.interfaces import IContained, IContainer

import sqlalchemy as rdb

metadata = rdb.MetaData()

class IUserContainer( IContainer ): pass
        
users = rdb.Table('users', metadata,
                  rdb.Column('user_id',
                             rdb.Integer,
                             rdb.Sequence('user_id_seq', optional=True),
                             primary_key = True),
                  rdb.Column('user_name', rdb.String(40), default=u'hello world' )
                  )

class SASchemaTests( TestCase ):

    def testSA2ZS( self ):
        
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

    def testInheritance( self ):
        class IUserBase( IContained ):
            def hello( ): pass
            
        iusers = transmute( users, bases=(IUserBase,) )
        class bar( object ):
            interface.implements( iusers )
            containers( IUserContainer )
        b = bar()
        
        self.assertTrue( IUserBase.providedBy( b ) )
        fields =  schema.getFieldsInOrder( iusers )

        for name, field in fields:
            assert name in ('user_id', 'user_name', '__name__')




def test_suite():
    from unittest import TestSuite, makeSuite
    suite=TestSuite()
    suite.addTest(makeSuite(SASchemaTests))
    return suite

if __name__ == '__main__':
    main()
        
                                
        
        

        
    
        
