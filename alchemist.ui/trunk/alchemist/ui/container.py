"""

$Id$
"""

from zope import schema, interface
from zope.publisher.browser import BrowserView
from zope.formlib import form
from zope.security import proxy
from zc.table import column, batching, table
from zc.table import table

import simplejson

from sqlalchemy import orm
from ore.alchemist.container import stringKey
from ore.alchemist.model import queryModelDescriptor, queryModelInterface
from i18n import _

import core

class Getter( object ):

    def __init__(self, getter):
        self.getter = getter

    def __call__( self, item, formatter):
        return self.getter( item )

def viewLink( item, formatter ):
    return u'<a class="button-link" href="%s">View</a>'%( stringKey( item ) )

def editLink( item, formatter ):
    return u'<a class="button-link" href="%s/edit">Edit</a>'%( stringKey( item ) )

def viewEditLinks( item, formatter ):
    return u'%s %s'%(viewLink( item, formatter), editLink( item, formatter ) )


class ContainerListing( form.DisplayForm ):
    
    form_fields = form.Fields()
    mode = "listing"
    
    def update( self ):
        context = proxy.removeSecurityProxy( self.context )
        columns = core.setUpColumns( context.domain_model )
        columns.append(
            column.GetterColumn( title = _(u'Actions'),
                                 getter = viewEditLinks )
            )
        self.columns = columns
        
        super( ContainerListing, self).update()
        
    def render( self ):
        return self.index()
        
    def listing( self ):
        return self.formatter()
    
    @property
    def formatter( self ):
        context = proxy.removeSecurityProxy( self.context )
        
        formatter = table.AlternatingRowFormatter( context,
                                                   self.request,
                                                   context.values(),
                                                   prefix="form",
                                                   columns = self.columns )
        formatter.cssClasses['table'] = 'listing'
        formatter.table_id = "datacontents"
        return formatter
        

    @property
    def form_name( self ):
        return "%s %s"%( self.context.domain_model.__name__, self.mode.title())

    @form.action(_(u"Add") )
    def handle_add( self, action, data ):
        self.request.response.redirect('add')


class ContainerJSONListing( BrowserView ):
    """
    paging, batching, sorting, json contents of a container
    """

    def getSort( self ):
        """ server side sort,
        @web_parameter sort - request variable for sort column
        @web_parameter dir  - direction of the sort, only once acceptable value 'desc'
        """
        sort_key, sort_dir = self.request.get('sort'), self.request.get('dir')
        
        # get sort in sqlalchemy form
        if sort_key and ( sort_key in self.context.domain_model.c ):
            column = self.context.domain_model.c[sort_key]
            if sort_dir == 'desc':
                return getattr( column, sort_dir )
            return column
        return None
    
    def getOffsets( self ):
        nodes = []
        start, limit = self.request.get('start',0), self.request.get('limit', 0)
        try:
            start, limit = int( start ), int( limit )
            if not limit:
                limit = 100
        except ValueError:
            start, limit = 0, 100
        return start, limit 

    def getBatch( self, start, limit, order_by=None):
        batch = []

        domain_interface = queryModelInterface( self.context.domain_model )
        domain_interface = proxy.removeSecurityProxy( domain_interface )
        field_names = schema.getFieldNamesInOrder( domain_interface )

        # fetch the nodes from the container
        nodes = self.context.batch( offset=start,
                                    limit=limit,
                                    order_by=order_by )
        
        for n in nodes:
            d = {}
            # field to dictionaries
            for f in field_names:
                field = domain_interface[ f ]
                d[ f ] = field.query( n )
            batch.append( d )
        return batch
        
    def __call__( self ):
        start, limit = self.getOffsets( )
        sort_clause = self.getSort()
        batch = self.getBatch( start, limit, sort_clause )
        set_size = len( self.context )
        data = dict( length=set_size, nodes=batch )
        return simplejson.dumps( data )
