"""
defines schema annotations for ui information

transforms sqlalchemy table definitions into zope 3 schemas
using the annotation.

modifies the domain classes to attach the schema interface 

$Id$
"""

from zope.interface import Interface
from ore.alchemist.annotation import TableAnnotation
from ore.alchemist.sa2zs import transmute

import schema

PersonAnnotation = TableAnnotation(
    "Person",
    columns = [
         dict( name="first_name", label = "First Name", table_column=True ),
         dict( name="middle_initial", label = "Middle Initial", table_column=True ),         
         dict( name="last_name", label = "Last Name",  table_column=True ),
         dict( name="email", label = "Email Adddress", table_column=True ),
         dict( name="phone_number", label = "Home Phone Number"),
         ]
    )

AddressAnnotation = TableAnnotation(
    "Address",
    columns = [
        dict( name="address_1", label = "Address Line 1"),
        dict( name="address_2", label = "Address Line 2"),
        ]
    )


IPersonTable = transmute( schema.PersonTable,
                          PersonAnnotation,
                          __module__="Products.orgperson.interfaces" )

IAddressTable = transmute( schema.AddressTable,
                           AddressAnnotation,
                           __module__="Products.orgperson.interfaces" )

                  
class IPersonContainer( Interface ):
    """ marker iface for generic containers """
