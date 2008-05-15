from setuptools import setup, find_packages

setup(
    name="alchemist.ui",
    version="0.3.0",
    install_requires=['setuptools', 'ore.alchemist', 'zope.formlib', 'zope.viewlet'],
    packages=find_packages(exclude=["*.tests"]),
#    package_dir= {'':'src'},
    namespace_packages=['alchemist'],
    package_data = {
      '': ['*.txt', '*.zcml', '*.pt'],
    },
    zip_safe=False,
    author='Kapil Thangavelu',
    author_email='kapil.foss@gmail.com',
    description="""\
alchemist.ui contains generic user interface components for use
with achemist.core based systems.
""",
    license='LGPL',
    keywords="zope zope3",
    )
