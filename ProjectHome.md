Provides a series of python packages of zope components for using relationally stored data. These packages try to mirror most of the common primitives in zope used against persistent objects. Additional packages also provide support for Plone
and Zope2 primitives.

Features -

> - includes zope3 sqlalchemy database and session transaction integration.

> - automatic sqlalchemy session management

> - bidirectional schema transformation, from zope3 schemas to sqlalchemy, and from sqlalchemy tables to zope3 schemas.

> - zope.schema.vocabulary support

> - container and application support

> - traversal patterns for applications and containers for date and attribute based urls.

> - property validation on sqlalchemy mapped objects based on zope.schema

> - zope.formlib, zc.table based generic user interface on sqlcontainers and objects, including embedded related display.

> - zope3 catalog and zc.relations support via ( keyreference adapters / intid support )

Separate Plone/Zope2 Packages provide

> - pas authentication, search plugins

> - membership integration, with per schema management and automatically generated registration, preferences forms (ore.member)

> - a more efficient archetypes sqlstorage that aggregates per transaction reads and writes across fields, based on an orm peer implementation.

> - an auditlog implementation that stores content changes and state into a relational database. effectively configurably syncing a plone's content with a relational database.