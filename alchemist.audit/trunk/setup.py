import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()
    
setup(
    name="ore.xapian",
    version="0.4.2",
    install_requires=['setuptools',
                      'ore.alchemist',
                      'zope.security',
                      'zope.lifecycleevent'],
    packages=find_packages('src'),
    package_dir= {'':'src'},
    namespace_packages=['ore'],
    package_data = {
    '': ['*.txt', '*.zcml'],
    },
    zip_safe=False,
    classifiers = [
        'Intended Audience :: Developers',
        'Framework :: Zope3'
        ],
    url="https://svn.objectrealms.net/svn/public/ore.xapian/",
    keywords="zope3 index search xapian xappy",
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    description="A Xapian Content Indexing/Searching Framework for Zope3",
    long_description=(
        read('src','ore','xapian','readme.txt')
        + '\n\n' +
        read('changes.txt')
        + '\n\n'
        ),
    license='GPL',
    keywords="zope zope3",
    )


setup(
    name="alchemist.security",
    version="0.4.1-dev",    
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    description="Relational Implementation of Zope Security components",
    long_description="""
    A relational implementation of zope security components, including
    authentication, principal role mappings (global and local),
    permission role mappings ( global and local ).
    """,
    license='ZPL',
    keywords="zope zope3",
    classifiers=['Programming Language :: Python',
                 'Environment :: Web Environment',
                 "License :: OSI Approved :: Zope Public License",                 
                 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                 'Framework :: Zope3',
                 ],    
    install_requires=['setuptools', 'ore.alchemist', 'zope.securitypolicy'],
    packages=find_packages(exclude=["*.tests"]),
    namespace_packages=['alchemist'],
    package_data = {
      '': ['*.txt', '*.zcml'],
    },
    zip_safe=False,
    )
