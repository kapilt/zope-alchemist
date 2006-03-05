"""
A SQLAlchemy Archetypes Storage, using peers


Author: Kapil Thangavelu <kapil@objectrealms.net>
Copyright (c) 2006 ObjectRealms, LLC
$Id$
"""

from Products.Archetypes.public import StorageLayer
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

        if self.isInitialized( content ) or \
           getattr( instance, "_at_is_fake_instance", None):
            return 

        peer = self.getPeerFor( instance )

    def cleanupInstance( self, instance, item=None, container=None):
        # don't delete on move, fake, or not initialized instance
        if getattr( instance, '_v_cp_refs' None) \
           or getattr( instance, "_at_is_fake_instance", None) \
           or not self.isInitialized( instance ):
            return

        peer = self.getPeerFor( instance )
        # delete

    def get(self, name, instance, **kargs):
        if not self.isInitialized( instance ):
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

    def getPeer(self, instance ):
        alchemist = getToolByName( instance, AlchemistTool.id  )
        factory = alchemist.getPeerFactory( instance )
        peer = factory.get( uid = instance.UID() ) or factory()
        return peer
