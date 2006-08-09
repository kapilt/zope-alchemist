"""
$Id$
"""

from unittest import TestCase, main

from sqlalchemy import * # to hard to fight ;-)
from ore.alchemist import changeset
from ore.alchemist.engine import get_engine
from ore.alchemist import introspector

import transaction

engine = get_engine( 'mysql://root@localhost/alchemy', echo=True)

metadata = BoundMetaData( engine )

other_metadata = DynamicMetaData()


users = Table('users', metadata,
                            Column('user_id', Integer, Sequence('user_id_seq', optional=True), primary_key = True),
                            Column('user_name', String(40)),
                            )


other_users = Table('users', other_metadata,
                                  Column('user_id', Integer, Sequence('user_id_seq', optional=True), primary_key = True),
                                  Column('user_name', String(40)),
                                  Column('fullname',  String(90)),
                                  )


addresses = Table('email_addresses', metadata,
                      Column('address_id', Integer, Sequence('address_id_seq', optional=True), primary_key = True),
                      Column('user_id', Integer, ForeignKey(users.c.user_id)),
                      Column('email_address', String(40)),
                  )

other_addresses = Table('email_addresses', other_metadata,
                            Column('address_id', Integer, Sequence('address_id_seq', optional=True), primary_key = True),
                            Column('email_address', String(40)),
                        )



orders = Table('orders', metadata,
                   Column('order_id', Integer, Sequence('order_id_seq', optional=True), primary_key = True),
                   Column('user_id', Integer, ForeignKey(users.c.user_id)),
                   Column('description', String(50)),
                   Column('isopen', Integer),

                   )

other_orders = Table('orders', other_metadata,
                         Column('order_id', Integer, Sequence('order_id_seq', optional=True), primary_key = True),
                         Column('user_id', Integer, ForeignKey(users.c.user_id)),
                         Column('description', String(50)),
                         Column('isopen', Integer),

                         )


orderitems = Table('items', metadata,
                       Column('item_id', INT, Sequence('items_id_seq', optional=True), primary_key = True),
                       Column('order_id', INT, ForeignKey("orders")),
                       Column('item_name', VARCHAR(50)),

                       )

metadata.create_all()

cset = changeset.changeset( metadata, other_metadata )

try:
    cset.introspect()
except:
    import pdb, traceback, sys
    ec = sys.exc_info()
    traceback.print_exception( *ec )
    pdb.post_mortem( ec[-1] )

print "Changes"
cset.pprint()
    
transaction.commit()
