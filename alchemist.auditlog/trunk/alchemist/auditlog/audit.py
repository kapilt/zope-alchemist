"""
Auditing of Changes for Domain Objects
"""
from datetime import datetime

from zope import component, interface, schema
from zope.security.management import checkPermission, getInteraction
from zope.publisher.interfaces import IRequest

from zope import lifecycleevent
from ore.alchemist import Session
from ore.alchemist.interfaces import IRelationChange
from sqlalchemy import orm

from zope.component.zcml import subscriber, adapter

import interfaces
import sqlalchemy as rdb
import features

# event subscribers to capture application changes to objects

class AuditFeature( object ):

    def __init__( self, change_table, change_klass ):
        self.change_table = change_table
        self.change_klass = change_klass
        
class ItemVersions( object ):
    """a collection of the versions of a parliamentary content object
    """
    @classmethod
    def makeVersionFactory( klass, name ):
        return type( name, (klass,), {} )            
        
def make_changes_table( table, metadata ):
    """ create an object log table for an object """
    table_name = table.name
    entity_name =  table_name.endswith('s') and table_name[:-1] or table_name
    
    changes_name = "%s_changes"%( entity_name )
    fk_id = "%s_id"%( entity_name )
    
    changes_table = rdb.Table(
            changes_name,
            metadata,
            rdb.Column( "change_id", rdb.Integer, primary_key=True ),
            rdb.Column( fk_id, rdb.Integer, rdb.ForeignKey( table.c[ fk_id ] ) ),
            rdb.Column( "action", rdb.Unicode(16) ),
            rdb.Column( "date", rdb.DateTime, default=rdb.PassiveDefault('now') ),
            rdb.Column( "description", rdb.Unicode),
            rdb.Column( "notes", rdb.Unicode),
            rdb.Column( "user", rdb.Integer, rdb.ForeignKey('users.user_id') ),
    )
    
    return changes_table        

class ChangeRecorder( object ):

    def __init__( self, change_table ):
        self.change_table = change_table

    def objectAdded( self, object, event ):
        self._objectChanged(u'added', object )
    
    def objectModified( self, object, event ):
        attrset =[]
        for attr in event.descriptions:
            if lifecycleevent.IAttributes.providedBy( attr ):
                attrset.extend(
                    [ attr.interface[a].title for a in attr.attributes]
                    )
            elif IRelationChange.providedBy(attr):
                attrset.append( attr.description )

        description = u", ".join( attrset )
        self._objectChanged(u'modified', object, description )
        
    def objectDeleted( self, object, event ):
        self._objectChanged(u'deleted', object )

    def _objectChanged( self, change_kind, object, description=u'' ):
        oid, otype = self._getKey( object )
        user_name = self._getCurrentUserName()

        self.changes_table.insert(
            values = dict( kind = change_kind,
                           date = datetime.now(),
                           user_name = user_name,
                           description = description,
                           content_type = otype,
                           content_id = oid )
            ).execute()
        
    def _getKey( self, ob ):
        mapper = orm.object_mapper( ob )
        primary_key = mapper.primary_key_from_instance( ob )[0]
        return primary_key, unicode( ob.__class__.__name__ )

    def _getCurrentUserName( ):
        interaction = getInteraction()
        for participation in interaction.participations:
            if IRequest.providedBy(participation):
                return participation.principal.title
        raise RuntimeError(_("No IRequest in interaction"))    

def GenerateChangeFeature( ctx ):

    feature = features.featureFilter( ctx.descriptor, interfaces.IAuditFeature )
    if not feature:
        return
        
    recorder = ChangeRecorder( feature.change_table )
    
    # setup subscribers for audit log
    subscriber( ctx.zcml, 
                for_=( lifecycleevent.IObjectModifiedEvent, ctx.domain_interface )
                handler=recorder.objectModified )
                
    subscriber( ctx.zcml, 
                for_=( lifecycleevent.IObjectCreatedEvent, ctx.domain_interface )
                handler=recorder.objectAdded )
                
    subscriber( ctx.zcml, 
                for_=( lifecycleevent.IObjectCreatedEvent, ctx.domain_interface )
                handler=recorder.objectModified,
                )
    
    # setup views for change log
