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

from zope.component import getAdapter
from zope.interface import implementedBy
from zc.table import table

from ore.alchemist.interfaces import IModelAnnotation, IIModelInterface
from ore.alchemist import named

from Products.Five import BrowserView
from Products.alchemist.container import AlchemistContainer

class ContainerAddingView:

    """Add view for alchemist container view.
    """

    def __call__(self, add_input_name='', domain_class='', title='', submit_add=''):
        
        if not submit_add or not domain_class:
            return self.index()

        obj = AlchemistContainer( add_input_name, domain_class, title  )
        self.context.add(obj)
        self.request.response.redirect(self.context.nextURL())
        return ''


class ContainerView( BrowserView ):

    def __init__(self, context, request):
        super( ContainerView, self).__init__( context, request )

        model_iface = None
        # xxx single model interface domains implementations..
        for iface in implementedBy( context.domain_model ):
            if IIModelInterface.isImplementedBy( iface ):
                model_iface = iface
                break
        if model_iface is None:
            raise SyntaxError("domain model has no domain interfaces")
        
        self.info = getAdapter( model_iface, IModelAnnotation, named( model_iface ) )
        
    def _getTable( self ):
        columns = self.info.getDisplayColumns()
        results = self.context.values()

        return table.StandaloneFullFormatter( self.context,
                                              self.request,
                                              results,
                                              visible_column_names = [c.name for c in columns],
                                              columns = columns )
                                              
    table = property( _getTable )
    
        
