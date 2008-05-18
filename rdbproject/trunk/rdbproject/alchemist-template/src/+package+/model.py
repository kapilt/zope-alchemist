
from sqlalchemy import orm
from zope import interface

import schema
import interfaces

class User( object ):

    interface.implements( interfaces.IUser )
    
    def checkPassword( self, *args, **kw):
        return True

orm.mapper( User, schema.users )
    

