"""
a decorating mapper for sqlalchemy that utilizes field properties for attribute validation

-- pass on set and structs
-- currently has issues with fk references
"""

from bind import bindClass
from sqlalchemy import mapper

def bind_mapper( klass, *args, **kw):
    klass_mapper = mapper( klass, *args, **kw )
    bindClass( klass, klass_mapper )
    
    return klass_mapper
