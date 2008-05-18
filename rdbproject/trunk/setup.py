from setuptools import setup, find_packages

long_description = (open('README.txt').read()
                    + '\n\n' +
                    open('CHANGES.txt').read())

setup(
    name='rdbproject',
    version='0.3.0dev',
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    url='http://code.google.com/p/zope-alchemist',
    description="""
    Script that sets up an alchemist project directory, installs Zope3, Alchemist and
    creates a template for a alchemist application.""",
    long_description=long_description,
    license='ZPL',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['PasteScript>=1.6', 'zc.buildout'],
    tests_require=['zope.testing', 'zc.buildout', 'Cheetah', 'PasteScript'],
    test_suite='tests.test_suite',
    entry_points={
    'console_scripts': ['grokproject = rdbproject:main'],
    'paste.paster_create_template': ['alchemist = rdbproject:AlchemistProject']},
    )
