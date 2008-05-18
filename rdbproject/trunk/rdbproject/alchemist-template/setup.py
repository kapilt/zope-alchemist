from setuptools import setup, find_packages

setup(
    name="clincruit",
    version="0.2",
    author='Clincruit Developers',
    author_email='kapilt@gmail.com',
    description='Public Funds Tracking',
    keywords = "zope3 pft",
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
    packages=find_packages(),
    package_data = { '': ['*.txt', '*.zcml'] },
    install_requires = [ 'setuptools',
                         'SQLAlchemy',
                         'simplejson',
                         'zope.schema',
                         'zope.interface',
                         'zope.i18n',
                         'alchemist.ui',
                         'alchemist.security',
                         'ore.alchemist',
                         'ore.wsgiapp',
                         'z3c.menu.ready2go'
                         ],
    zip_safe = False,
    )

