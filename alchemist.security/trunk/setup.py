from setuptools import setup, find_packages

setup(
    name="alchemist.security",
    version="0.2.0",
    install_requires=['setuptools', 'ore.alchemist'],
    packages=find_packages(exclude=["*.tests"]),
#    package_dir= {'':'src'},
    namespace_packages=['alchemist'],
    package_data = {
      '': ['*.txt', '*.zcml', '*.pt'],
    },
    zip_safe=False,
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    description="z3 security components with relational storage",
    license='LGPL',
    keywords="zope zope3",
    )
