Versions
========

  >>> import alchemist.version
  
Set up the versions factory.
  
  >>> component.provideAdapter(
  ...    alchemist.version.ContextVersioned,
  ...    (alchemist.version.interfaces.IVersionable,),
  ...    alchemist.version.interfaces.IVersioned)  

Adding a question.

  >>> question = add_content(
  ...     domain.Question,
  ...     short_name="A question",
  ...     type="question",
  ...     language="en")

The ``question`` object needs to provide the versionable interface.
  
  >>> from zope.interface import alsoProvides
  >>> alsoProvides(question, alchemist.version.interfaces.IVersionable)

Verify that no versions exist yet:

  >>> versions =  alchemist.version.interfaces.IVersioned(question)
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
