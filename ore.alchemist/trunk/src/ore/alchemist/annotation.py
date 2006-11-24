##################################################################
#
# (C) Copyright 2006 ObjectRealms, LLC
# All Rights Reserved
#
# This file is part of Alchemist.
#
# Alchemist is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Alchemist is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CMFDeployment; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##################################################################
"""
Annotations for Table objects, to annotate as needed, the notion

is that the annotation keys correspond to column, and values correspond
to application specific column metadata.

$Id$
"""

from zope.interface import implements
from interfaces import IModelAnnotation
from sqlalchemy.util import OrderedDict
    
class ModelAnnotation( object ):
    
    implements( IModelAnnotation )
    
    def __init__(self, context, annotation):
        self.context = context
        self.annotation = annotation

    def getDisplayColumns(self):
        from zc.table.column import GetterColumn        
        columns = []
        for i in self.annotation.values():
            if i.get('table_column') is not True:
                continue
            def getter( ob, format, name=i['name']):
                return getattr( ob, name )
            column = GetterColumn( title = i['label'],
                                   name = i['name'],
                                   getter = getter )
            columns.append( column )
        return columns

class TableAnnotation( object ):

    #__slots__ = ("table_name", "_annot", "_options")

    def __init__(self, table_name, columns=None):
        self.table_name = table_name
        self._options = {}
        self._annot = OrderedDict()
        if columns:
            for info in columns:
                self._annot[ info['name'] ] = info

    def setOption( self, name, value ):
        self._options[ name ] = value
        
    def getOption( self, name, default=None ):
        return self._options.get( name, default )
    
    def __call__( self, context ):
        return ModelAnnotation( context, self )

    def __setitem__(self, name, value ):
        self._annot[name] = value

    def get( self, name, default=None ):
        return self._annot.get( name, default )

    def __getitem__(self, anme):
        return self.get( name )

    def values( self ):
        return self._annot.values()

    def __contains__(self, name ):
        marker = object()
        return not marker == self.get( name, marker )
