from zope import component
from zope.security.management import getInteraction
from zope.security.proxy import removeSecurityProxy
from zope.publisher.interfaces import IRequest

from zope import lifecycleevent
from datetime import datetime

from ore.alchemist.interfaces import IRelationChange
from ore.alchemist.model import queryModelInterface
from sqlalchemy import orm

import interfaces
from i18n import _

def provideRecorder( klass, change_table ):
    domain_interface = queryModelInterface( klass )
    recorder = type( "%sChangeRecorder"%(klass.__name__),
                     (ChangeRecorder,),
                     {'change_table':change_table} )
    component.provideAdapter( recorder, (domain_interface,), (interfaces.IRecorder,))
    
class ChangeRecorder( object ):

    change_table = None
    
    def __init__( self, context ):
        self.context = removeSecurityProxy(context)

    def objectAdded( self, event ):
        return self._objectChanged(u'added')
    
    def objectModified( self, event ):
        attrset =[]
        for attr in event.descriptions:
            if lifecycleevent.IAttributes.providedBy( attr ):
                attrset.extend(
                    [ attr.interface[a].title for a in attr.attributes]
                    )
            elif IRelationChange.providedBy(attr):
                attrset.append( attr.description )

        description = u", ".join( attrset )
        return self._objectChanged(u'modified', description )

    def objectStateChanged( self, event):
        description = _(u"""transition from %s to %s via %s - %s"""%( 
                        event.source,
                        event.destination,
                        event.transition.title,
                        event.comment ) )
        return self._objectChanged(u'workflow', description )
        
    def objectDeleted( self, event ):
        return self._objectChanged(u'deleted')

    def objectNewVersion( self, event ):
        return self._objectChanged(u"new-version", description=event.message )

    def objectRevertedVersion( self, event ):
        return self._objectChanged(u'reverted-version', description=event.message )
        
    def _objectChanged( self, change_kind, description=u'' ):
        oid, otype = self._getKey( self.context )
        user_id = self._getCurrentUserId()

        statement = self.change_table.insert(
            values = dict( action = change_kind,
                           date = datetime.now(),
                           user_id = user_id,
                           description = description,
                           content_type = otype,
                           content_id = oid )
            )
        value = statement.execute()
        return value.last_inserted_ids()[0]
        
    def _getKey( self, ob ):
        mapper = orm.object_mapper( ob )
        primary_key = mapper.primary_key_from_instance( ob )[0]
        return primary_key, unicode( ob.__class__.__name__ )

    def _getCurrentUserId( self ):
        interaction = getInteraction()
        for participation in interaction.participations:
            if IRequest.providedBy(participation):
                return participation.principal.id
        raise RuntimeError(_("No IRequest in interaction"))    
