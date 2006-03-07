from Products.CMFCore.utils import getToolByName

import config
from storage import AlchemistStorage

def getAlchemist( context ):
    return getToolByName( context, config.ALCHEMIST_TOOL )

def getStorageFields( context ):
    schema = context.Schema()
    return filter( lambda f: isinstance( f.storage, AlchemistStorage ),
                   schema.fields() )

def getDefaults( context ):
    defaults = {}
    for field in getStorageFields( context ):
        defaults[ field.getName() ] = field.getDefault( context )
    return defaults
