from setuptools import setup, find_packages

setup(
    name="alchemist.traversal",
    version="0.3.0",
    install_requires=['setuptools', 'ore.alchemist', 'z3c.traverser'],
    packages=find_packages(exclude=["*.tests"]),
#    package_dir= {'':'src'},
    namespace_packages=['alchemist'],
    package_data = {
      '': ['*.txt', '*.zcml', '*.pt'],
    },
    zip_safe=False,
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    description="""\
    various traversal mechanisms for alchemist containers and domain
    objects.
    """,
    license='LGPL',
    keywords="zope zope3",
    )
