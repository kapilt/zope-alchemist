

#from ore.alchemist.model import ModelFactory
#from ore.alchemist.modelio import ModelLoader
import transaction
from unittest import TestCase, main


class ModelIOTestCase( TestCase ):
    
    model = ModelFactory('mysql://root@localhost/alc2')
    
    def setUp( self ):
        self.loader = ModelLoader(  self.model )

    def tearDown( self ):
        transaction.abort()
        
    def testLoadYamlFile( self ):

        # load the model with database structures
        self.loader.fromFile('example.yaml')
        
        pfactory = self.model.getClassFor('persons')
        afactory = self.model.getClassFor('addresses')
        
        person = pfactory(first_name='ralph', email='john')
        address = afactory( name="Home Address")
        
        person.address = address
        transaction.commit()
        
        pid = person.person_id
        mid = id( pid )
        del person
        
        new_person_ref = pfactory.mapper.get( pid )

        self.assertNotEqual( id(new_person_ref), mid )
        self.assertEqual( new_person_ref.address.name, address.name )

if __name__ == '__main__':
    main()
