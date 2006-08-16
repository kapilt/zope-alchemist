"""
$Id$
"""

from yaml import load

from zope.dottedname.resolve import resolve
from zope.interface import implements

from annotation import TableAnnotation
from sa2zs import transmute, bindClass
from interfaces import IModelIO

class ModelLoader( object ):

    implements( IModelIO )

    def __init__(self, context ):
        self.context = context
        self.table_annotaions = {}
        self.state = {}
        
    def _tableDefaults( self ):
        pass

    def _columnDefaults( self ):
        pass

    table_defaults = property( _tableDefaults )

    column_defaults = property( _columnDefaults )

    def fromFile( self, file_path ):

        fh = open( file_path, 'r')
        fs = fh.read()
        fh.close()

        config = load( fs )
        self.fromStruct( config )
        
    def fromStruct( self, struct ):
        assert isinstance( struct, dict )
        self.setDefaults( strut )
        
        # load mapped and referenced tables
        for table_name, options in config.get('mappings', {}).items():
            self.context.loadTable( table_name )

        # load mappings in table order
        for table in self.context.metadata.table_iterator():
            
            # automatically loads a default mapper for each
            self.setupMapping( table_name, options['mappings'].get( table.name, {}) )

    def setupDefaults( self, config ):
        pass

    def setupMapping( self, table_name, options ):

        tannot = TableAnnotation( table_name )

        table_options = self.table_defaults.copy()
        table_options.update( options )

        tannot.setOption( "domain class", resolve( table_options['domain class'] ) )
        tannot.setOption( "interface module", resolve( table_options['interface module'] ) )
        tannot.setOption( "display columns", table_options.get('list display') )
        tannot.setOption( "omit-not-specified", table_options.get("omit-not-specified") )

        for column_name, options in options.get('columns', {}).items():
            self._setupColumn( tannot, column_name, options )

        self._defineClass( tannot )
        self._defineInterface( tannot )
        self._defineMapping( tannot )

    def _setupColumn( self, tannot, column_name, options ):
        column_options = self.column_defaults.copy()
        column_options.update( options )

        label = column_options.get('label')
        one_to_one = column_options.get('one to one')
        
        tannot[ column_name ] = column_options.get('label')
        tannot[ column_name ] 

    def _defineClass( self, tannot ):
        domain_class_path = tannot.options['domain class']
        marker = object()
        domain_class = resolve( domain_class_path, marker )

        if not domain_class:
            domain_class = resolve( tannot.options['default domain class'], marker )
            if not domain_class:
                raise RuntimeError("domain class not found, no default %s"%domain_class_path )
            domain_class = type( "%sDomainClass"%, (domain_class,), {})

        if not isinstance( domain_class, type):
            raise ProgrammingError("domain classes must be new style classes")
        
        tannot.domain_class = domain_class
        return domain_class
    
    def _defineInterface( self, tannot ):
        interface_module = tannot.options['interface module']
        tannot.interface = transmute( tannot.table, tannot, __module__=interface_module )
        return tannot.interface
        
    def _defineMapping( self, tannot ):

        
        # find all the related tables, infer one-2-one, many-2-many

        # iterate through table columns, find fks
        # establish
        pass


        
