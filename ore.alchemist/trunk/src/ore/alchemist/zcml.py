##############################################################################
#
# Copyright (c) 2008 Kapil Thangavelu <kapil.foss@gmail.com>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from zope import interface, schema
from zope.configuration.fields import GlobalObject

from zope import component
from zope.app.component.metaconfigure import utility, PublicPermission

import sqlalchemy
import interfaces

class IEngineDirective( interface.Interface ):
    """ Creates A Database Engine. Database Engines are named utilities.
    """
    url = schema.URI( title = u'Database URL',
                      description = u'SQLAlchemy Database URL',
                      required = True,
                      )
    
    name = schema.Text( title = u'Engine Name',
                        description = u'Empty if this engine is the default engine.',
                        required = False,
                        default = u'',
                        )
    
    echo = schema.Bool( title = u'Echo SQL statements',
                        description = u'Debugging Echo Log for Engine',
                        required = False,
                        default=False
                        )

# keyword arguments to pass to the engine
IEngineDirective.setTaggedValue('keyword_arguments', True)

def engine(_context, url, name='', echo=False, **kwargs):

    component = sqlalchemy.create_engine( url, echo=echo, **kwargs )

    utility( _context,
             provides = interfaces.IDatabaseEngine,
             component = component,
             permission = PublicPermission,
             name = name )
             

class IBindDirective( interface.Interface ):
    """ Binds a MetaData to a database engine.
    """

    engine = schema.Text( title = u"Engine Name" )
    
    metadata = GlobalObject( title=u"Metadata Instance",
                             description = u"Metadata Instance to be bound" )
    
    
def bind( _context, engine, metadata ):

    def _bind( engine_name, metadata ):
        metadata.bind = component.getUtility( interfaces.IDatabaseEngine, engine )

    _context.action(
        discriminator = ('alchemist.bind', metadata ),
        callable = _bind,
        args = ( engine, metadata )
        )
    
        
