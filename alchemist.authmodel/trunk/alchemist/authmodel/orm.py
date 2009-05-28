import sqlalchemy as rdb
from sqlalchemy.orm import mapper, relation, column_property, deferred

import schema
import domain

# general representation of a person
mapper ( domain.Person, schema.users,
          properties={
             'fullname' : column_property(
                 (schema.users.c.first_name + u" " + 
                  schema.users.c.middle_name + u" " + 
                  schema.users.c.last_name).label('fullname')
                 ),
             'user_description':schema.users.c.description,
             'groups': relation( domain.GroupMembership )
             },
 )


mapper( domain.User, schema.users,
        polymorphic_on=schema.users.c.type,
        polymorphic_identity='user',
       )

# Groups
mapper( domain.Group, schema.groups,
        properties={
            'members': relation( domain.GroupMembership ),
            },
        polymorphic_on=schema.groups.c.type,
        polymorphic_identity='group'
        )

mapper( domain.GroupMembership, schema.user_group_memberships,
        properties={
            'user': relation( domain.User,
                              primaryjoin=rdb.and_(schema.user_group_memberships.c.user_id==schema.users.c.user_id ),
                              lazy=False ),
            'group': relation( domain.Group,
                               primaryjoin=schema.user_group_memberships.c.group_id==schema.groups.c.group_id,
                               lazy=False ),                              
            }
        )
