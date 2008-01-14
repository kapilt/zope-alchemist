
from xml.sax.saxutils import escape
from zope.schema.vocabulary import SimpleVocabulary
from zope.app.form.browser.widget import renderElement
import zope.app.form.browser as widgets

from ore.alchemist import Session

class URLDisplayWidget( widgets.URIDisplayWidget ):
    """
    default renders with empty text, causing issues
    """
    linkTarget = None

    def __call__(self):
        if self._renderedValueSet():
            content = self._data
        else:
            content = self.context.default
        if not content:
            return u''
        content = escape(content)
        kw = dict(contents=content, href=content)
        if self.linkTarget:
            kw["target"] = self.linkTarget
        return renderElement("a", **kw)    
    
class LongTextWidget( widgets.TextWidget ):

    displayWidth = 60

class YesNoDisplayWidget( widgets.DisplayWidget ):

    def __call__(self):
        if self._renderedValueSet():
            value = self._data
        else:
            value = self.context.default
        if value:
            return u"Yes"
        else:
            return u"No"

def YesNoInputWidget(field, request, true='Yes', false='No'):
    vocabulary = SimpleVocabulary.fromItems( ((true, True), (false, False)) )
    widget = widgets.RadioWidget(field, vocabulary, request)
    widget.size = 2
    widget.required = False
    return widget    

class NamedFkGetter( object ):
    def __init__( self, attribute, model ):
        self.attribute = attribute
        self.model = model
        
    def __call__( self, item, formatter ):
        value = getattr( item, self.attribute, None)
        if value is None:
            return None
        #return IModelDescriptor( object ).title
        associated = Session().get( self.model, value)
        return associated.short_name
