"""
defines schema annotations for ui information

transforms sqlalchemy table definitions into zope 3 schemas
using the annotation.

modifies the domain classes to attach the schema interface 

$Id$
"""

from zope.interface import Interface, directlyProvides
from ore.alchemist.annotation import TableAnnotation
from ore.alchemist.sa2zs import transmute
from zope import schema as zschema
from zope.schema.interfaces import IContextSourceBinder

import schema
from vocabulary import StateVocabulary


AddressAnnotation = TableAnnotation(
    "Address",
    columns = [
        dict( name="address_id", omit = True ), # omit means that the we never see the id in the schema
        dict( name="address_1", label = "address line 1"),
        dict( name="address_2", label = "address line 2"),
        ],
    properties = {'state':zschema.Choice( title=u"state", vocabulary=StateVocabulary() ) }
    )

IAddressTable = transmute( schema.AddressTable,
                           AddressAnnotation,                           
                           __module__="Products.orgperson.interfaces" )


PersonAnnotation = TableAnnotation(
    "Person",
    columns = [
         dict( name="first_name", label = "First Name" ),
         dict( name="middle_initial", label = "Middle Initial" ),         
         dict( name="last_name", label = "Last Name" ),
         dict( name="email", label = "Email Address" ),
         dict( name="phone_number", label = "Home Phone Number" ),
         dict( name="address_id", omit = True ),
         dict( name="person_id", omit = True )
         ],
# you can specify which columns should be in the container listing view via this, first column
# always links to record
        table_columns = ('first_name', 'last_name', 'email', 'phone_number'), 
# you can specify the order of the fields globally via this mechanism
#    schema_order = ('email', 'phone_number'),
    properties = {'address':zschema.Object( IAddressTable, required=False ) },    
    )

                  

IPersonTable = transmute( schema.PersonTable,
                          PersonAnnotation,
                          __module__="Products.orgperson.interfaces" )


class IPersonContainer( Interface ):
    """ marker interface for adding app specific views and adapters to generic containers """
