
from zope.interface import Interface

class IAlchemySchemaModel( Interface ):


    def __getitem__( key ):
        """
        return the peer factor for the given key or None
        """

    def loadType( archetype_klass, context ):
        """
        load the schema from the given archetype klass,
        translate it to an alchemy model, and alchemy
        mapped peer class, uses context as an acquisition
        context if nesc.
        """

    def loadInstance( instance ):
        """
        
        """
        