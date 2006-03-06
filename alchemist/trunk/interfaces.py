from zope.interface import Interface


class IAlchemySchemaModel( Interface ):

    def match( object ):
        """
        should this model be used for the given object
        """

    def clear( ):
        """
        clear all loaded state for the model
        """

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
        as above but load from an instance...

        does not support context based schemas.. need to
        qualify the name on storage.
        """
        
