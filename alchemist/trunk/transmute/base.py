

class AlchemistTranslation( object ):

    def __init__( self, primary_table, relation_tables=(), properties=None ):

        self.table = primary_table
        self.relation_tables = relation_tables
        self.properties = properties
        
