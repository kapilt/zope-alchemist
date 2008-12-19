import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="alchemist.ui",
    version="0.4.1",
    install_requires=['setuptools',
                      'ore.alchemist',
                      'zope.formlib',
                      'zc.table',
                      'zope.viewlet',
                      'simplejson'],
    packages=find_packages(exclude=["*.tests"]),
    namespace_packages=['alchemist'],
    package_data = {
      '': ['*.txt', '*.zcml', '*.pt'],
    },
    zip_safe=False,
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    description="user interface components for use with zope3 relational database applications, crud, listing and relation views",
    long_description = read('changes.txt'),
    license='LGPL',
    classifiers=['Programming Language :: Python',
                 'Framework :: Zope3',
                 ],        
    keywords="zope zope3",
    )
