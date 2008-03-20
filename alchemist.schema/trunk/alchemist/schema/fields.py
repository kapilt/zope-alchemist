

from zope import schema
from ore.alchemist.model import Field

class FieldDefinition( object ):
    
    def __init__( self, *args, **kw ):
        self._mfield = Field.fromDict( kw )
        map( kw.__delitem__, self._mfield.consumed)
        super( FieldDefinition, self).__init__( *args, **kw )
        
    @property
    def model_field( self ):
        return self._mfield
        
class Int( FieldDefinition, schema.Int ): pass
class Float( FieldDefinition, schema.Float ): pass
class Decimal( FieldDefinition, schema.Decimal ): pass
class Bool( FieldDefinition, schema.Bool ): pass

class Text( FieldDefinition, schema.Text): pass
class TextLine( FieldDefinition, schema.TextLine): pass
class ASCII( FieldDefinition, schema.ASCII ): pass
class ASIILine( FieldDefinition, schema.ASCIILine): pass
class Bytes( FieldDefinition, schema.Bytes ): pass
class BytesLine( FieldDefinition, schema.BytesLine ): pass

class Datetime( FieldDefinition, schema.Datetime ): pass
class Date( FieldDefinition, schema.Date ): pass
class Timedelta( FieldDefinition, schema.Timedelta ): pass
class Time( FieldDefinition, schema.Time): pass

class Choice( FieldDefinition, schema.Choice): pass
class Password( FieldDefinition, schema.Password ): pass


