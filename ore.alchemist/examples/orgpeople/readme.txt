=========================================
building relational applications wih zope 
=========================================


Requirements
------------

 runtime environment
 - mysql 5.+ ( 4.1 might work, but not officially supported )

 zope2 products

 - plone 2.5
 - alchemist
 - Five 1.4
 - CMFonFive ( for actions support )

 zope3 python libraries

 - ore.alchemist
 - zc.table
 - zc.resourcelibrary
 - zc.datetime
 

Defining the Model
------------------

 a walkthrough by file of defining the application's object model.

 - define the application's database tables/structure( person.sql )

 - introspect the database to load into the application the database
   tables/structure metadata. ( schema.py )

 - translate our database metadata into an application consumable form by converting them
   to zope3 interfaces so we can address them and utilize platform
   infrastructure. additionally we use annotations on the database
   structures to add additional semantic information 
   useful for the user interface. ( interfaces.py )

 - define classes consisting of the application domain model ( domain.py )

 - map classes to database structures ( mapper.py )

we now have a core application model that we where we can manipulate
objects to change the database. 

everything we done this to point is zope agnostic, and we can utilize
standalone python scripts to manipulate the model and we haven't
needed to write a single line of sql.

Accessing Objects through the web
---------------------------------

an alchemist container object is added to instance space and
associated with a domain class and allows for direct url traversal to
domain objects. (extensions/install.py)

Construcing User Interfaces
---------------------------

now we need to put up our application specific user interface.

Five allows us to utilize zope3 technology to construct views for our
object and associate them via interface. Everything is interface driven.

since we have zope3 interfaces for our domain model, out of the box,
utilizing zope 3 technologies, we get for free automatically generated
add and edit forms for any domain objects. to associate application
specific views. (configure.zcml)

to allow for attaching model specific container views, we decorate the alchemist
container with our application specific marker interfaces.  
(extensions/install.py  and configure.zcml IPersonContainer)


