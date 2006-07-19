"""
$Id$
"""
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase

ZopeTestCase.installProduct("alchemist")

from unittest import TestCase, main

import transaction

from Products.alchemist.engine import get_engine
from Products.alchemist.model import pas
import sqlalchemy as rdb

class TestAlchemistPAS( TestCase ):

    def setUp(self):
        transaction.begin() # just insures an abort before we begin

    def tearDown(self):
        transaction.get().abort()

    def testPASModel(self):

        try:
            engine = get_engine("postgres://database=alchemy", echo=True )
        except:
            import pdb, sys
            ec = sys.exc_info()
            pdb.post_mortem( ec[-1])
        model = pas.PlonePASModel(engine)
        parts = model.generateDefaults()

        engine.create_tables()
        
        test_user = parts['User']('test_user')
        test_role = parts['Role']('test_role')
        test_role.name = "MonkeyRole"
        test_user.roles.append( test_role )
        

        
        for i in test_role.users:
            print i

        test_group = parts['Group']('test_group')
        
        test_group.roles.append( test_role )

        for i in test_role.groups:
            print i

        class ns(object):
            def __init__(self, d):
                self.d = d
                
            def __getattr__(self,name):
                return self.d[name]

        m = ns( parts )

        pid = 'test_user'
        select_user_roles =rdb.select( [m.roles.c.name.label('role_name')],
                rdb.and_(
            m.user_role_map.c.role_id == m.roles.c.role_id,
            m.user_role_map.c.user_id == pid )
                )

        print select_user_roles
        res = select_user_roles.execute( user_role_map_user_id = pid )
        print len(res)
        for r in res:
            print r


if __name__ == '__main__':
    main()

    
