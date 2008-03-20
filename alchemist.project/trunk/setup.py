from setuptools import setup, find_packages


setup(
    name='alchemist.project',
    version='0.3.1',
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    url='http://cheeseshop.python.org/pypi/zopeproject',
    download_url='http://code.google.com/projects/zope-alchemist/downloads',
    description='Tools and Scripts for Creating Relational Zope3 Applications',
    long_description="insert long description",
    license='ZPL',
    classifiers=['Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Zope Public License',
                 'Programming Language :: Python',
                 'Topic :: Internet :: WWW/HTTP :: WSGI',
                 'Framework :: Zope3',
                 ],

    packages=find_packages(),
    namespace_packages=['alchemist'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['PasteScript>=1.3',],
    entry_points="""
    [console_scripts]
    rdbproject = alchemist.project.main:rdbproject
    [paste.paster_create_template]
    rdb_deploy = alchemist.project.templates:RDBDeploy
    rdb_app = alchemist.project.templates:RDBApp
    """,
)
