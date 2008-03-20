from setuptools import setup, find_packages

setup(name='alchemist.server',
      version='0.2',
      description="server packaging, deployment, startup of alchemist zope3 server",
      long_description="",
      keywords='',
      author='Kapil Thangavleu',
      author_email='kapil.foss@gmail.com',
      url='http://code.google.com/p/zope-alchemist',
      license='ZPL',
      # Get more from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Environment :: Web Environment',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                   'Framework :: Zope3',
                   ],

      packages=find_packages(),
      namespace_packages=['alchemist'],
      include_package_data=True,
      zip_safe=True,
      install_requires=['setuptools',
                        'ZODB3',
                        'ZConfig',
                        'zdaemon',
                        'zope.publisher',
                        'zope.traversing',
                        'zope.app.wsgi>=3.4.0',
                        'zope.app.appsetup',
                        'zope.app.zcmlfiles',
                        # The following packages aren't needed from the
                        # beginning, but end up being used in most apps
                        'zope.annotation',
                        'zope.copypastemove',
                        'zope.formlib',
                        'zope.i18n',
                        'zope.app.authentication',
                        'zope.app.session',
                        'zope.app.intid',
                        'zope.app.keyreference',
                        'zope.app.catalog',
                        # The following packages are needed for functional
                        # tests only
                        'zope.testing',
                        'zope.app.testing',
                        'zope.app.securitypolicy',
                        'ore.wsgiapp',
                        ],
      entry_points = """
      [paste.app_factory]
      main = alchemist.server.startup:application_factory
      """
      )
