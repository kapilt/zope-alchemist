
 Alchemist

  Zope(2||3) & Plone database integration based on the sqlalchemy database
  toolkit for python. It is designed to offer access and enhance
  sqlalchemy's utilizing Zope3 technology for use within or *without*
  a Zope runtime.

 Features

  Core 

   - sqlalchemy zope transaction integration

   - on the fly creation of zope3 schemas from sqlalchemy tables

   - automatic add/edit/view for mapped objects

   - validation for relational attributes based on introspected schema definition.

   - generic containers with view customization via marker interfaces

   - database introspectors

   - no inheritance requirements for domain classes, all zope integration is interface based.

   - designed to work with existing databases.

  Model - In Development

   - yaml based mapping and configuration 

   - automatic (basic only) and configurable relationship detection

   - better generic views

   - database schema/aspect behaviors


 Milestone 1 - Core Features -Listed above, these obsolete a number of the milestone
 0 features.

 Milestone 0 - Core Features - most of these are obsolete they were done
  against an older version of sqlalchemy (0.16), when the focus of
  alchemist was different, alchemist as exists today (8/1/2006) is
  currently focused on programatic developer access utilizing zope3
  technologies (wo zope runtimes), and these older features which
  utilize archetypes need updating.

  Runtime translation of archetypes schemas to sqlalchemy relational
  tables and mappers.

  Efficient archetypes storage, with intelligent aggregation of loads 
  and store operations.

  Zope transaction integration.

  Works with any kind of archetype object.

  Provides through the web schema development tools.

 

 Credits

  Kapil Thangavelu <hazmat@objectrealms.net> - Author - http://objectrealms.net

  Michael Bayer - SQLAlchemy Author - http://sqlalchemy.org

