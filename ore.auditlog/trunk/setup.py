from setuptools import setup, find_packages

setup(
    name="ore.auditlog",
    version="0.3",
    packages=find_packages('src'),
    package_dir= {'':'src'},
    namespace_packages=['ore'],
    package_data = { '': ['*.txt', '*.zcml'] },
    zip_safe=False,
    author='ObjectRealms',
    author_email='kapilt@objectrealms.net',
    description="""\
ore.auditlog is a package for recording changes to content to a relational database
""",
    license='BSD',
    keywords="zope zope3",
    classifiers = ['Framework :: Plone'],
    install_requires=['setuptools'],
    )
