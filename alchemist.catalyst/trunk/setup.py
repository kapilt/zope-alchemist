from setuptools import setup, find_packages

setup(
    name="alchemist.catalyst",
    version="0.4.0dev",
    install_requires=['setuptools', 'ore.alchemist', 'alchemist.ui', 'alchemist.traversal', "SQLAlchemy==0.4.4"],
    packages=find_packages(exclude=["*.tests"]),
    #package_dir= {'':'src'},
    namespace_packages=['alchemist'],
    package_data = {
      '': ['*.txt', '*.zcml', '*.pt'],
    },
    zip_safe=False,
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    description="""\
directed, automatic creation of user interfaces and domain objects for relational applications.
""",
    license='LGPL',
    keywords="zope zope3",
    )
