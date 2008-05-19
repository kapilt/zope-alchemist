from setuptools import setup, find_packages

long_description = (open('README.txt').read()
                    + '\n\n' +
                    open('CHANGES.txt').read())

setup(
    name='rdbproject',
    version='0.3.1-dev',
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    url='http://code.google.com/p/zope-alchemist',
    description="""Paster Template for Alchemist/Zope3 Projects"
    long_description = long_description,
    license='ZPL',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['PasteScript>=1.6', 'zc.buildout'],
    tests_require=['zope.testing', 'zc.buildout', 'Cheetah', 'PasteScript'],
    test_suite='tests.test_suite',
    entry_points={
    'console_scripts': ['rdbproject = rdbproject:main'],
    'paste.paster_create_template': ['alchemist = rdbproject:AlchemistProject']},
    )
