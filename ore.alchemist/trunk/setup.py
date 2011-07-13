from setuptools import setup, find_packages

def read( name ):
    return open( name ).read()

setup(
    name="ore.alchemist",
    version="0.6.0",
    url="http://code.google.com/p/zope-alchemist",
    install_requires=['setuptools', 
                      'transaction', 
                      'SQLAlchemy', 
                      "zope.app.container", 
                      "zope.app.testing",
                      'zope.sqlalchemy'],
    packages=find_packages('src', exclude=["*.tests"]),
    package_dir= {'':'src'},
    namespace_packages=['ore'],
    package_data = {
    '': ['*.txt', '*.zcml', '*.pt'],
    },
    zip_safe=False,
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    description="sqlalchemy zope3 integration",
    long_description="""\
ore.alchemist provides core features for zope3 relational database applications
utilizing sqlalchemy. it includes transformation of zope3 schemas to sqlalchemy
tables,  sqlalchemy transformation into zope3 schemas, and containers.

it maintains a minimal api for sqlalchemy abstraction, you can use
whatever constructions sqlalchemy supports.

additionally ore.alchemist is the foundation package for a range of additional
services, including a range of user interface components and widgets for
interacting with domain models. more information can be found on the project's
homepage.
""" + '\n\n' + read('changes.txt'),
    license='ZPL',
    keywords="zope zope3",
    )
