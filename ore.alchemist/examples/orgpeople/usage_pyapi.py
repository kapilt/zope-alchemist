#################################
# Inserting Records 
#################################
# Table Model
"""
using the table models. sqlalchemy provides multiple usage modes, you can utilize
what you need.
"""
import schema
import transaction

# create an insert statement against this table
i = schema.PersonTable.insert()

# qualify it with values and execute
i.execute( first_name="peter",
           last_name="rabbit",
           email="peter.rabbit@example.com")

# let's say we have an error, we can abort using zope's transaction api (txa)
transaction.abort()

i.execute( first_name="mary",
           last_name="rabbit",
           email="mary.rabbit@example.com")

# commit the transaction.
transaction.commit()








# Object Model
"""

using the object model api, we can just use simple attribute access

"""


import domain
import mapper

# create a new empty person record
person = domain.Person()

# specify some attributes
person.last_name = u"wolf"
person.email = u"mrwolf@example.com"

address = domain.Address( name=u"conference", city=u"Alexandria", state=u"VA")

person.address = address

# because of the backref we can use either endpoint to get to the other.
# ie. we get bidirectional references.
#
print "Person name", address.person.last_name == 'wolf'

# commit the transaction
transaction.commit()


#################################
# Querying Objects
#################################


# session accessor api
from ore.alchemist.manager import get_session

# get the current session
object_session = get_session()

# create a person query
query = object_session.query( domain.Person )

# query by email
print query.select_by_email(u'mrwolf@example.com')[0].last_name


