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
        context = proxy.removeSecurityProxy( self.context )
        
        formatter = batching.Formatter( context,
                                            self.request,
                                            context.values(),
                                            prefix="form",
                                            visible_column_names = [c.name for c in self.columns],
                                            columns = self.columns )
        
        #formatter.mapper = [pk.name for pk in orm.class_mapper( context.domain_model )]
        formatter.cssClasses['table'] = 'listing'
        formatter.table_id = "datacontents"
        return formatter()

    @property
    def form_name( self ):
        return "%s %s"%( self.context.domain_model.__name__, self.mode.title())

    @form.action(_(u"Add") )
    def handle_add( self, action, data ):
        self.request.response.redirect('add')


class ContainerJSONListing( BrowserView ):
    """
    paging, batching, json contents of a container
    """

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

    def getBatch( self, start, limit ):
        batch = []
        nodes = self.context.batch( start, limit)
        
        domain_interface = queryModelInterface( self.context.domain_model )
        domain_interface = proxy.removeSecurityProxy( domain_interface )
        field_names = schema.getFieldNamesInOrder( domain_interface )

        for n in nodes:
            d = {}
            for f in field_names:
                field = domain_interface[ f ]
                d[ f ] = field.query( n )
            batch.append( d )
        return batch
        
    def __call__( self ):
        start, limit = self.getOffsets( )
        batch = self.getBatch( start, limit )
        set_size = len( self.context )
        data = dict( length=set_size, nodes=batch )
        return simplejson.dumps( data )
