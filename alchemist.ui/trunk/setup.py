from setuptools import setup, find_packages

setup(
    name="alchemist.ui",
    version="0.3.0",
    install_requires=['setuptools'],
    packages=find_packages('src', exclude=["*.tests"]),
    package_dir= {'':'src'},
    namespace_packages=['ore'],
    package_data = {
      '': ['*.txt', '*.zcml', '*.pt'],
    },
    zip_safe=False,
    author='ObjectRealms, LLC',
    author_email='info@objectrealms.net',
    description="""\
alchemist.ui contains generic user interface components for use
with achemist.core based systems.
""",
    license='GPL',
    keywords="zope zope3",
    )
