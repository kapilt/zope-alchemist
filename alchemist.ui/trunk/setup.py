from setuptools import setup, find_packages

setup(
    name="alchemist.ui",
    version="0.3.2",
    install_requires=['setuptools', 'ore.alchemist', 'zope.formlib', 'zc.table', 'zope.viewlet'],
    packages=find_packages(exclude=["*.tests"]),
    namespace_packages=['alchemist'],
    package_data = {
      '': ['*.txt', '*.zcml', '*.pt'],
    },
    zip_safe=False,
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    description="user interface components for use for zope3 database applications, crud and relation views",
    license='LGPL',
    keywords="zope zope3",
    )
