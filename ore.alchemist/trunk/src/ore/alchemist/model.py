"""
$Id$
"""
from zope.interface import Interface, implements
from ore.alchemist import named

from sqlalchemy import mapper, BoundMetaData, Table
from sa2zs import transmute, bindClass

class IAlchemistModel( Interface ):

    def __getitem__( self, table_name ):
        """
        return the associated domain class for the given table name
        """


    def loadFile( file_path ):
        """
        load a yaml file containing configuration
        """

    #################################
    # private?
    def load( table_set=() ):
        """
        load domain mappings from the specified set of table names or annotations, if
        none are passed in, then load for all the database tables.
        """

    def loadTable( table_spec ):
        """
        load and return the given table 
        """

    def loadInterface( table_spec ):
        """
        load the given interace
        """

    def defineInterface( table_spec ):
        """
        """

    def defineMapper( domain_class, table_spec, **kw):
        """
        """

class IMapperFactory( Interface ):
    pass

class ModelSpecification( object ):

    def __init__(self, mapping, domain_class, table_interface, table):
        self.mapping = mapping
        self.domain_class = domain_class
        self.interface = table_interface
        self.table = table

    def __call__(self, *args, **kw):
        return self.domain_class( *args, **kw )

from ore.alchemist.engine import get_engine

def ModelFactory( db_uri ):
    db = get_engine( db_uri )
    meta = BoundMetaData( db )
    return AppModel( meta )

class AppModel( object ):

    implements( IAlchemistModel, IMapperFactory )
    
    def __init__(self, metadata):
        self.interfaces = {} # name to iface
        self.mappers = {} # class name to mapper
        self.tables = {} # table name to table
        self.table_classes = {} # table name to class name
        self.klasses = {} # class name to class
        self.metadata = metadata
        self.compiled = False 

    def loadFile( self, file_path ):
        loader = IModelIO( self )
        loader.fromFile( file_path )
        self.compile()
        
    def defineMapping( self, annotated_table, **kw ):
        table_mapper = mapper( annotated_table.domain_class, annotated_table.table, **kw)
        self.mappers[ named( annotated_table.domain_class ) ] = table_mapper
        annotated_table.domain_class.mapper = table_mapper
        self.table_classes[ annotated_table.table.name ] = annotated_table.domain_class

    def defineInterface(self, annotated_table, module=None):
        annotated_table.interface = i = transmute( annotated_table.table,
                                                   annotated_table,
                                                   __module__ = module )
        

    def loadTable( self, table_name ):
        if table_name in self.tables:
            return self.tables[ table_name ]
        self.tables[ table_name ] = Table( table_name, self.metadata, autoload=True )
        return self.tables[table_name]

    def loadMapping( self, domain_class, domain_table, **kw ):
        self.klasses[ named( domain_class ) ] = domain_class
        self.tables[ named( domain_table ) ]  = domain_table
        mapper = mapper( domain_class, domain_table, **kw)
        self.mappers[ named( domain_class ) ] = mapper
        return mapper

    def addMapping( self, mapping ):
        self.klasses[ named( mapping.class_ ) ] = mapping.class_
        self.mappers[ named( mapping.class_ ) ] = mapping

    def getMappingFor( self, class_name=None, table_name=None ):
        pass

    def getClassFor( self, table_name ):
        return self.table_classes[ table_name ]
    
    def compile( self ):
        pass
