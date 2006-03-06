from Products.CMFCore.utils import getToolByName

import config

def getAlchemist( context ):
    return getToolByName( context, config.ALCHEMIST_TOOL )

