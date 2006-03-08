"""
$Id$
"""

from unittest import TestCase, main

from sqlalchemy import objectstore
from sqlalchemy import * # to hard to fight ;-)
import sqlalchemy as rdb


from engine import create_engine
from changeset import SchemaChangeSet


import transaction

engine = create_engine( 'zpgsql://database=alchemy', echo=True)
engine.do_zope_begin()

other_engine = create_engine( 'zpgsql://database=alchemy', echo=True)


users = Table('users', engine,
              Column('user_id', Integer, Sequence('user_id_seq', optional=True), primary_key = True),
              Column('user_name', String(40)),
              )

other_users = Table('users', other_engine,
              Column('user_id', Integer, Sequence('user_id_seq', optional=True), primary_key = True),
              Column('user_name', String(40)),
              Column('fullname',  String(90)),              
              )


addresses = Table('email_addresses', engine,
    Column('address_id', Integer, Sequence('address_id_seq', optional=True), primary_key = True),
    Column('user_id', Integer, ForeignKey(users.c.user_id)),
    Column('email_address', String(40)),
)

other_addresses = Table('email_addresses', other_engine,
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

other_orders = Table('orders', other_engine,
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

engine.create_tables()

import pdb; pdb.set_trace()
transaction.commit()
