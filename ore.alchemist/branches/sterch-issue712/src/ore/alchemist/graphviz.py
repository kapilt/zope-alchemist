##############################################################################
#
# Copyright (c) 2006-2008 Kapil Thangavelu <kapil.foss@gmail.com>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
really simple visualizer.. transform models to graph viz.
"""

from cStringIO import StringIO

class ModelVisualizer( object ):

    def __init__( self, metadata ):
        self.metadata = metadata
        self.io = StringIO()
        
    def dot( self ):

        io = self.io
        
        print >> io, "digraph database {"
        tables = set()
        mapping_table = set()
        
        for t in self.metadata.table_iterator():
            options = []
            is_mapping = len(t.foreign_keys) == 2 and len( t.columns ) == 2
            
            if is_mapping:
                options.append( 'color=red')
            else:
                options.append( 'color=blue')
                
            is_vocabulary = len( t.foreign_keys ) == 0
            
            tables.add(
                ( t.name, is_vocabulary, is_mapping )
                )
                
            for f in t.foreign_keys:
                destination = f.column.table.name
                print >> io, '  %s -> %s [label="%s", %s];'%(
                    t.name, destination, f.parent.name, ', '.join(options))

        for name, is_vocabulary, is_mapping in tables:
            if is_mapping:
                print >> io, " %s [color=red];"%(name)
            if is_vocabulary:
                print >> io, " %s [color=green];"%(name)
            else:
                print >> io, " %s [shape=box];"%(name)
            
        print >> io, "}"
        
        return io.getvalue()

    def tofile( self, filename):
        fh = open( filename, 'w' )
        fh.write( self.dot() )
        fh.flush()
        fh.close()
        
