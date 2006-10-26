
import domain

# we do our binding here.. need to import for effects, alternative structure
# suggest for real world, use, for didatic purposes here, we have things separated out.
# and manually import. patterns emerging.. suggestions on recommended welcome.

import mapper

import transaction

from unittest import TestSuite, makeSuite, TestCase, main
from zope.schema.interfaces import WrongType

from datetime import datetime 

class OrgPersonTests( TestCase ):

    def test_Validation( self ):
        
        person = domain.Person(email=u"kapil@objectrealms.net")
        try:
            person.address_id = "abc"
        except WrongType:
            pass
        else:
            raise AssertionError("failed type check")

        person.last_name = u"thangavelu"
        person.first_name = u"kapil"
        try:
            person.created = "abc"
        except WrongType:
            person.created = datetime.now()
        else:
            raise AssertionError("failed date type check")
        
        
if __name__ == '__main__':
    main()
