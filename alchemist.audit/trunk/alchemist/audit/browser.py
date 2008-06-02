
from zope.publisher.browser import BrowserView
from zope.security.proxy import removeSecurityProxy
from zc.table import batching, column

import sqlalchemy as rdb
from sqlalchemy import orm

import interfaces

from i18n import _

class ChangeBaseView( BrowserView ):
    """
    base view for looking at changes to context
    """
    
    formatter_factory = batching.Formatter
    
    columns = [
        column.GetterColumn( title=_(u"action"), getter=lambda i,f:i['action'] ),    
        column.GetterColumn( title=_(u"date"), getter=lambda i,f: i['date'] ),
        column.GetterColumn( title=_(u"user"), getter=lambda i,f:i['user_id'] ),
        column.GetterColumn( title=_(u"description"), getter=lambda i,f:i['description'] ),
        ]    
    
    def listing( self ):
        columns = self.columns
        formatter = self.formatter_factory( self.context,
                                            self.request,
                                            self.getFeedEntries(),
                                            prefix="results",
                                            visible_column_names = [c.name for c in columns],
                                            #sort_on = ('name', False)
                                            columns = columns )
        formatter.cssClasses['table'] = 'listing'
        formatter.updateBatching()
        return formatter()
        
    @property
    def _log_table( self ):
        auditor = interfaces.IRecorder( self.context )
        return auditor.change_table
        
    def getFeedEntries( self ):
        instance = removeSecurityProxy( self.context )        
        mapper = orm.object_mapper( instance )
        
        query = self._log_table.select().where(
            rdb.and_( self._log_table.c.content_id == rdb.bindparam('content_id') )
            )

        content_id = mapper.primary_key_from_instance( instance )[0] 
        content_changes = query.execute( content_id = content_id )
        return map( dict, content_changes)

class ChangeLog( ChangeBaseView ):
    """
    Change Log View for an object
    """
    form_name = "Change Log"
