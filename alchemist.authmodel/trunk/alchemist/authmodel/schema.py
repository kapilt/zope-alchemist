
import sqlalchemy as rdb
from datetime import datetime

metadata = rdb.MetaData()

PrincipalSequence = rdb.Sequence('principal_sequence') # for users and groups because of the zope users and groups

#######################
# Users 
#######################

users = rdb.Table(
   "users",
   metadata,
   rdb.Column( "user_id", rdb.Integer, PrincipalSequence, primary_key=True ),
   rdb.Column( "login", rdb.Unicode(16), unique=True, nullable=True ),
   rdb.Column( "first_name", rdb.Unicode(80), nullable=False ),
   rdb.Column( "last_name", rdb.Unicode(80), nullable=False ),
   rdb.Column( "middle_name", rdb.Unicode(80) ),
   rdb.Column( "email", rdb.String(32), nullable=False ),
   rdb.Column( "password", rdb.String(36)), # we store salted md5 hash hexdigests
   rdb.Column( "salt", rdb.String(24)),  
   rdb.Column( "active_p", rdb.Boolean(), default=True ),
   rdb.Column( "type", rdb.String(30), nullable=False  ),
   )

#######################
# Groups
#######################

groups = rdb.Table(
   "groups",
   metadata,
   rdb.Column( "group_id", rdb.Integer, PrincipalSequence,  primary_key=True ),
   rdb.Column( "short_name", rdb.Unicode(40), nullable=False ),
   rdb.Column( "full_name", rdb.Unicode(80) ),   
   rdb.Column( "description", rdb.UnicodeText ),
   rdb.Column( "status", rdb.Unicode(12) ), # workflow for groups
   rdb.Column( "start_date", rdb.Date, nullable=False ),
   rdb.Column( "end_date", rdb.Date ),  #
   rdb.Column( "type", rdb.String(30),  nullable=False )
   )

#######################
# Group Memberships encompasses any multiple types of  participation in a group and can be workflowed
#######################

user_group_memberships = rdb.Table(
   "user_group_memberships",
   metadata,
   rdb.Column( "membership_id", rdb.Integer,  primary_key=True),
   rdb.Column( "user_id", rdb.Integer, rdb.ForeignKey( 'users.user_id')),
   rdb.Column( "group_id", rdb.Integer, rdb.ForeignKey( 'groups.group_id')),
   rdb.Column( "start_date", rdb.Date, default=datetime.now, nullable=False ),
   rdb.Column( "end_date", rdb.Date ),
   rdb.Column( "status", rdb.String(30) ),
   rdb.Column( "active_p", rdb.Boolean, default=True ),
   # type of membership 
   rdb.Column( "membership_type", rdb.String(30), default ="member")
   )
