##################################################################
#
# (C) Copyright 2006 ObjectRealms, LLC
# All Rights Reserved
#
# This file is part of Alchemist.
#
# Alchemist is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Alchemist is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CMFDeployment; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##################################################################
"""
$Id$
"""

from zope.interface import Interface, Attribute
from zope.schema import TextLine, Choice
from ore.alchemist.interfaces import IAlchemistContainer

class IZopeSimpleItem( Interface ):
    add_input_name = TextLine( title=u"Id")
    title = TextLine( title=u"Title", required=False)
    
class IAlchemistIntrospector( Interface ):
    introspector = Attribute(u"introspector", u"volatile introspector implementation")
    engine_uri = Choice( title=u"Engine URI", vocabulary="Alchemist Available Engines")    
    schema = TextLine( title=u"Schema", required=False )

class IAlchemistWorkbench( Interface ):
    pass


    


                             



    
