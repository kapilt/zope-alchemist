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
$Id$
"""

from zope.formlib import form
from zope.component import getAdapter

from Products.Five import BrowserView
from Products.Five.formlib import formbase
from Products.Bling.ajax import jsonify

from Products.alchemist.introspector import AlchemistIntrospector
from Products.alchemist.interfaces import IAlchemistIntrospector, IZopeSimpleItem

class IntrospectorAddingView( formbase.AddFormBase ):

    form_fields = form.Fields( IZopeSimpleItem, for_input= True )
    form_fields += form.Fields( IAlchemistIntrospector, for_input=True)
    
    def create(self, data):
        # using formlib, name is form prefixed, stuff it directly onto
        # the adding view for processing by add
        self.context.contentName = data['add_input_name']
        return AlchemistIntrospector( data['add_input_name'],
                                      data.get('title', u''),
                                      str(data['engine_uri']),
                                      data.get('schema', None) )

    def nextURL( self ):
        return self.context.absolute_url() + "/" + self.context.contentName
    
class IntrospectorBrowserView( BrowserView ):

    def tableListing( self ):
        for table_name in self.context.introspector.orderedKeys():
            yield self.context.introspector.itemInfo( table_name )

    def tableDetails( self, table_name ):
        return self.context.introspector.itemInfo( table_name )

    def tableGraph( self ):
        pass

class IntrospectorTableView( IntrospectorBrowserView ):

    def table(self):
        name = self.request.get('table_name')
        if not name:
            self.request.response.redirect( context.absolute_url() )
        return self.context.introspector[ name ]

    
class IntrospectorJSONView( IntrospectorBrowserView ):

    tableListing = jsonify( IntrospectorBrowserView.tableListing )

    tableDetails = jsonify( IntrospectorBrowserView.tableDetails )    

    tableGraph = jsonify( IntrospectorBrowserView.tableGraph )

class IntrospectorGraphvizView( BrowserView ):
    pass

    


