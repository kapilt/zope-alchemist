
from engine import get_engine
from model import pas

import sqlalchemy as rdb

from model.pas import PlonePASModel
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin


_Model = None


class PASAlchemist( BasePlugin ):

    def __init__(self, id, dburi, title=''):
        self.id = id
        self.title = title
        self.dburi = dburi


    def activate(self):
        global _Model
        if _Model is not None:
            engine = get_engine( self.dburi )
            _Model = PlonePASModel( engine )
            _Model.generateDefaults()

    def model(self):
        return _Model

    def getPropertiesForUser( self, user, request=None ):
        pass

    def getGroupsForPrincipal(self, principal, request=None ):
        pass

    def getRolesForPrincipal( self, principal, request=None ):

        pid = principal.getId()
        
        rdb.select( [m.roles.name.label('role_name')],
                    rdb.and_(
                        m.user_role_map.role_id == m.roles.role_id,
                        m.user_role_map.user_id == pid )
                    )
                    
                
        self.model().user_role_map


    def setPropertiesForUser(self, user):
        pass
    
    #   IGroupEnumerationPlugin implementation
    #
    #security.declarePrivate( 'enumerateGroups' )
    def enumerateGroups( self
                        , id=None
                        , title=None
                        , exact_match=False
                        , sort_by=None
                        , max_results=None
                        , **kw
                        ):
        pass
    
    


                           
if __name__ == '__main__':
    model = PlonePASModel()
    parts = model.generateDefaults()

    test_user = parts['User']('test_user')
    test_role = parts['Role']('test_role')
    test_user.roles.append( test_role )

    for i in test_role.users:
        print i

    test_group = parts['Group']('test_group')

    test_group.roles.append( test_role )

    for i in test_role.groups:
        print i
        
