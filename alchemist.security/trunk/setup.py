from setuptools import setup, find_packages


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
