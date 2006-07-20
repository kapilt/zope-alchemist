"""
$Id$
"""

from zope.interface import Interface
from zope.schema import TextLine


class IAlchemistContainer( Interface ):
    """
    a domain record container
    """

    title = TextLine(
        title = u"Title",
        description =u"The title of the object",
        default = u"",
        required = False
        )

    domain_class = TextLine(
        title = u"Domain Class",
        description = u"The Python Path of the Domain Class",
        default = u"Products.alchemist.domain.DomainRecord",
        required = True
        )



    
