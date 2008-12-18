import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="alchemist.traversal",
    version="0.4.0",
    install_requires=['setuptools', 'ore.alchemist', 'z3c.traverser'],
    packages=find_packages(exclude=["*.tests"]),
    namespace_packages=['alchemist'],
    package_data = {
      '': ['*.txt', '*.zcml', '*.pt'],
    },
    zip_safe=False,
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    description="""Foreign Key Traversal mechanisms for alchemist containers and domain objects.""",
    long_description="Traversal of objects by foreign keys for relational applications"+'\n\n'+read('changes.txt'),
    license='LGPL',
    classifiers=[
                 'Framework :: Zope3',
                 ],        
    keywords="zope zope3",
    )
