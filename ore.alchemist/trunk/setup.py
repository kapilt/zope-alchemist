from setuptools import setup, find_packages

setup(
    name="ore.alchemist",
    version="0.5.0",
    url="http://code.google.com/p/zope-alchemist",
    install_requires=['setuptools', 'transaction'],
    packages=find_packages('src', exclude=["*.tests"]),
    package_dir= {'':'src'},
    namespace_packages=['ore'],
    package_data = {
    '': ['*.txt', '*.zcml', '*.pt'],
    },
    zip_safe=False,
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    description="""\
ore.alchemist contains an integration of sqlalchemy into the
Zope App server environment. It can be used with Zope2, Zope3 or
standalone.
""",
    license='ZPL',
    keywords="zope zope3",
    )
