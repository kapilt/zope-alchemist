"""
A SQLAlchemy Archetypes Storage, using peers


Author: Kapil Thangavelu <kapil@objectrealms.net>
Copyright (c) 2006 ObjectRealms, LLC
$Id$
"""

import config

from Products.Archetypes.Storage import StorageLayer
from Products.CMFCore.utils import getToolByName

class AlchemistStorage( StorageLayer ):

    def getName(self):
        return self.__class__.__name__

    def initializeField(self, instance, field):
        pass

    def unset(self, name, instance, **kwargs):
        pass
    
    def cleanupField( self, instance, field):
        pass

    def initializeInstance(self, instance, item=None, container=None):

        if self.isInitialized( instance ) or \
           getattr( instance, "_at_is_fake_instance", None):
            return 

        peer = self.getPeerFor( instance )
        instance.__initialized = True
        return peer

    def cleanupInstance( self, instance, item=None, container=None):
        # don't delete on move, fake, or not initialized instance
        if getattr( instance, '_v_cp_refs', None) \
           or getattr( instance, "_at_is_fake_instance", None) \
           or not self.isInitialized( instance ):
            return

        peer = self.getPeerFor( instance )
        # delete

    def get(self, name, instance, **kwargs):
        if not self.isInitialized( instance ):
            if 'field' in kwargs:
                return kwargs['field'].default
            return None
        peer = self.getPeerFor( instance )
        return getattr( peer, name )

    def set(self, name, instance, value, **kwargs):
        if not self.isInitialized( instance ):
            return None

        peer = self.getPeerFor( instance )
        setattr( peer, name, value )

    def isInitialized(self, content):
        return getattr( content, '__initialized', False )

    def getPeerFor(self, instance ):
        alchemist = getToolByName( instance, config.ALCHEMIST_TOOL  )
        peer = alchemist.getPeerFor( instance )
        return peer
