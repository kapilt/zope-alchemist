from zope import interface, schema

class IManagedContainer( interface.Interface ):
    """
    """

class IConstraintManager( interface.Interface ):

    """
    manages the constraints on a managed container
    """
    
    def setConstrainedValues( instance, target ):
        """
        ensures existence of conformant constraint values
        to match the query.
        """
        
    def getQueryModifier( instance, container ):
        """
        given an instance inspect for the query to retrieve 
        related objects from the given alchemist container.
        """    

        