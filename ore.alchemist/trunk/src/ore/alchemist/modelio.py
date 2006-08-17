"""
$Id$
"""

from yaml import load

from zope.dottedname.resolve import resolve
from zope.interface import implements

from sqlalchemy import relation

from annotation import TableAnnotation
from sa2zs import transmute, bindClass
from interfaces import IModelIO
from domain import DomainRecord

class ModelLoader( object ):

    implements( IModelIO )

    def __init__(self, context ):
        self.context = context
        self.table_annotaions = {}
        self.state = {}
        
    def _tableDefaults( self ):
        return {'domain class':'ore.alchemist.domain.DomainRecord',
                'interface module':'generated.interfaces',
                'display columns' : None,
                'omit-not-specified': False }

    def _columnDefaults( self ):
        return {}

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
        self.setupDefaults( struct )
        
        # load mapped and referenced tables
        for table_name, options in struct.get('mappings', {}).items():
            table = self.context.loadTable( table_name )

        # load mappings in table order
        for table in self.context.metadata.table_iterator( reverse=False ):
            
            # automatically loads a default mapper for each
            self.setupMapping( table.name, struct['mappings'].get( table.name, {}) )

    def setupDefaults( self, config ):
        pass

    def setupMapping( self, table_name, options ):

        tannot = TableAnnotation( table_name )
        tannot.table = self.context.metadata.tables[ table_name ]
        table_options = self.table_defaults.copy()
        table_options.update( options )

        tannot.setOption( "domain class", resolve( table_options['domain class'] ) )
        #tannot.setOption( "interface module", resolve( table_options['interface module'] ) )
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

#        label = column_options.get('label')
#        one_to_one = column_options.get('one to one')
        
        tannot[ column_name ] = column_options

    def _defineClass( self, tannot ):
        #domain_class_path = 
        marker = object()
        domain_class = tannot.getOption('domain class')
        if domain_class is DomainRecord:
            domain_class = type( "%sDomainClass"%(tannot.table.name,), (domain_class,),{})

        if not isinstance( domain_class, type):
            raise ProgrammingError("domain classes must be new style classes")
        
        tannot.domain_class = domain_class
        return domain_class
    
    def _defineInterface( self, tannot ):
        interface_module = tannot.getOption('interface module')
        for fk in tannot.table.foreign_keys:
            print fk
            
        tannot.interface = transmute( tannot.table, tannot, __module__=interface_module )
        return tannot.interface
        
    def _defineMapping( self, tannot ):
        attributes = {}
        
        # find all the related tables and infer basic relations, this sort of crude
        # inference should be optional.
        for fk in tannot.table.foreign_keys:

            klass = self.context.getClassFor( table_name = fk.column.table.name )
            attr_name = tannot.get( fk.column.name ).get('attribute', fk.column.table.name )
            backref   = tannot.get( fk.column.name ).get('backref', tannot.table.name )
            
            attributes[ attr_name ] = relation( klass, backref=backref )
            
##             # if fk is a primary key then model as inheritance
##             if fk.column.primary_key:
##                 klass = self.getClassFor( fk.column.table.name )
##                 raise NotImplemented

##             # if fk is to another table and the constraint is not unique
            
##             # if fk is to a mapping table then as a m2m, mapping determined
##             # by fk 2 column ratio

        self.context.defineMapping( tannot, properties=attributes )
        



        
