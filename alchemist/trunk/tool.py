
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import UniqueObject

from modeler import AlchemistModeler


class AlchemistTool( UniqueObject, AlchemistModeler ):

    meta_type = "Alchemist Tool"
    id = "portal_alchemist"
    security = ClassSecurityInfo()

    def __init__(self, *args, **kw):
        pass

