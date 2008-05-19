rdbproject provides an easy way to get started with a `Alchemist
<http://cheeseshop.python.org/pypi/ore.alchemist>`_ web applications.  

These applications are based on the Zope3 Framework, except they
rely on relational databases for a primary datastore.

Simply install ``rdbproject``::

  $ easy_install rdbproject

and run the ``rdbproject`` script with the name of the project you'd
like to create as an argument::

  $ rdbproject furcoat
  ... many lines of output here

This will not only create a project area for you to work in, it will
also download and install alchemist and Zope 3 (the application server
alchemist is built on).

If you specify a database module, you can also specify whether or not you
want to have buildout download and install it for you. 

After the project area has been created successfully, you will find an
a skeleton Python package in the ``src`` directory in which you can place
the code for your web application.  To start the server, execute
``bin/paster serve debug.ini``. The basic package includes some facilties
for login/logout, a little css, and some default template style.

For those who know paster: ``rdbproject`` is just a wrapper around a
paster template.  So instead of running the ``rdbproject`` command,
you can also run:

  $ paster create -t alchemist furcoat
