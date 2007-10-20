from zope import interface, schema

class IEngineDirective(interface.Interface):
    """ Creates A Database Engine. Database Engines are named utilities.
    """
    url = schema.URI( title = u'Database URL',
                      description = u'SQLAlchemy Database URL'
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
