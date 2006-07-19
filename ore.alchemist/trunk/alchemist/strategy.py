"""
zope sqlalchemy strategy

for now just utilize the thread local

$Id$
"""

from sqlalchemy.engine.strategies import ThreadLocalEngineStrategy, EngineStrategy

class ZopeEngineStrategy( ThreadLocalEngineStrategy ):
    def __init__(self):
        EngineStrategy.__init__(self, 'zope')

ZopeEngineStrategy()    
