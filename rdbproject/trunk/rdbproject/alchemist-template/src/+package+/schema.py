import sqlalchemy as rdb

metadata = rdb.MetaData()

# for users and groups because of the zope users and groups
PrincipalSequence = rdb.Sequence('principal_sequence')

users = rdb.Table(
   "users",
   metadata,
   rdb.Column( "user_id", rdb.Integer, PrincipalSequence, primary_key=True ),
   rdb.Column( "login", rdb.Unicode(16), unique=True, nullable=True ),
   rdb.Column( "first_name", rdb.Unicode(80), nullable=False ),
   rdb.Column( "last_name", rdb.Unicode(80), nullable=False ),
   rdb.Column( "middle_name", rdb.Unicode(80) ),
   rdb.Column( "email", rdb.String(32), nullable=False ),
    )

class Users( object ):

    def checkPassword( self, *args, **kw):
        return True

