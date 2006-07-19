"""
$Id$
"""

from Globals import UNIQUE
from OFS.SimpleItem import SimpleItem
from ExtensionClass import Base
from zope.interface import implements

from interfaces import IAlchemistTool

from Products.alchemist.engine import list_engines

class UniqueObject (Base):
    """ redefine to avoid cmf dep
    """
    __replaceable__ = UNIQUE

    def _setId(self,id):

        if id != self.getId():
            raise RuntimeError("can't change id")

class AlchemistTool( UniqueObject, SimpleItem):

    id = 'alchemist_plaything'
    
    implements( IAlchemistTool )
    

class AddingView:

    """Add view for demo content.
    """

    def listEngines(self):
        return list_engines()

    def __call__(self, add_input_name='', title='', submit_add=''):
        if submit_add:
            obj = AlchemistTool()
            self.context.add(obj)
            self.request.response.redirect(self.context.nextURL())
            return ''
        return self.index()
