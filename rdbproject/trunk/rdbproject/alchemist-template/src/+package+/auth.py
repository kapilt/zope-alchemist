"""
zope3 authenticator plugin against a relational database
"""

from zope import interface, component
from alchemist.security.interfaces import IAlchemistUser, IAlchemistAuth

import domain

@interface.implementer( IAlchemistUser )
@component.adapter( IAlchemistAuth )
def authUser( util ):
    return domain.User
