Versions
========

  >>> import bungeni.core.version

Set up the versions factory.
  
  >>> component.provideAdapter(
  ...    bungeni.core.version.ContextVersioned,
  ...    (bungeni.core.interfaces.IVersionable,),
  ...    bungeni.core.interfaces.IVersioned)  

Adding a question.

  >>> from bungeni.models.testing import add_content
  >>> from bungeni.models import domain

  >>> question = add_content(
  ...     domain.Question,
  ...     short_name="A question",
  ...     type="question",
  ...     language="en")

The ``question`` object needs to provide the versionable interface.
  
  >>> from zope.interface import alsoProvides
  >>> alsoProvides(question, bungeni.core.interfaces.IVersionable)

Verify that no versions exist yet:

  >>> versions =  bungeni.core.interfaces.IVersioned(question)
  >>> len(tuple(versions.values()))
  0  

After creating a version, verify availability:
  
  >>> version = versions.create('New version created ...')
  >>> len(tuple(versions.values()))
  1

Cleanup
-------

  >>> from ore.alchemist import Session
  >>> session = Session()
  
  >>> session.flush()
  >>> session.commit()
  >>> session.close()
