"""
$Id: $

based on zope.publisher.mapply adapted for class instantiation
and sa initialization hooks
"""

_marker = object()

def createInstance( klass, data ):
    """
    generically create an instance of a sqlalchemy object
    with a dictionary of data, and then return the instance
    and the remainder of the data. uses default args if found
    and no value for arg present in data.
    """
    func = klass.__init__.im_func
    func = func.func_dict.get('_oldinit', func)
    defaults = func.func_defaults
    
    names = func.func_code.co_varnames[1:]
    args = []
    used = []

    nrequired = len(names)
    if defaults:
        nrequired -= len( defaults )
    
    for i in range(len(names)):
        n = names[i]
        v = data.get(n, _marker)
        
        if v is _marker:
            if i < nrequired:
                raise TypeError("missing argument %s"%n)
            else:
                v = defaults[ i-nrequired ]
        else:
            used.append(n)
        args.append( v )
        
    for n in used:
        del data[n]

    ob = klass(*args)

    return ob
    

if __name__ == '__main__':
    from piston import model

    d = {'short_name':'b', 'extra':'2'}

    ob = generic( model.Agreement, d )
    assert tuple(d.keys()) == ('extra',)

    d = dict(short_name='a', status='True', security_level='a', extra=2)

    ob = generic( model.DataSource, d )
    assert tuple(d.keys()) == ('extra',)

    
    
    
