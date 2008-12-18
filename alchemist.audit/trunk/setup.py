import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()
    
setup(
    name="alchemist.audit",
    version="0.3.2",
    install_requires=['setuptools',
                      'ore.alchemist',
                      'zope.formlib',
                      'zc.table'],
    packages=find_packages(),
    namespace_packages=['alchemist'],
    package_data = {
    '': ['*.txt', '*.zcml'],
    },
    zip_safe=False,
    classifiers = [
        'Intended Audience :: Developers',
        'Framework :: Zope3'
        ],
    url="http://code.google.com/p/zope-alchemist",
    keywords="zope3 audit",
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    description="Alchemist Auditing Components ( Event Subscribers, Change Recorders, UI ) for Relational Applications",

    long_description=(
        read('alchemist','audit','readme.txt')
        + '\n\n' +
        read('changes.txt')
        + '\n\n'
        ),
    classifiers=['Programming Language :: Python',
                 'Framework :: Zope3',
                 ],        
    license='ZPL',
    )

