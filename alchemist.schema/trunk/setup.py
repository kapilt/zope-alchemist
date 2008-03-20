from setuptools import setup, find_packages

setup(
    name="alchemist.schema",
    version="0.2.0",
    install_requires=['setuptools', 'ore.alchemist'],
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
Allows usage of Zope3 Interface as DSL for application construction.
""",
    license='LGPL',
    keywords="zope zope3",
    )
