
class sqlite3:
    install_parts = ""
    parts = ""
    dbi_module = ""

class postgres:
    install_parts = "database database-ctl database-shell dbi-module"
    dbi_module = 'psycopg2'
    parts="""
[database]
recipe = zc.recipe.cmmi
url = http://ftp7.us.postgresql.org/pub/postgresql/source/v8.3.1/postgresql-8.3.1.tar.bz2

[database-ctl]
recipe = lovely.recipe:mkfile
path = ${buildout:bin-directory}/pg_ctl
mode = 0755
content =
 #!/bin/sh
 ${database:location}/bin/pg_ctl $*

[database-shell]
recipe = lovely:recipe:mkfile
path = ${buildout:bin-directory}/psql
mode = 0755
content =
 #!/bin/sh
 ${database:location}/bin/psql $*

[dbi-module]
egg = psycopg2
recipe = zc.recipe.egg:custom
find-links = http://www.initd.org/pub/software/psycopg/psycopg2-2.0.6.tar.gz
define = PSYCOPG_EXTENSIONS,PSYCOPG_DISPLAY_SIZE,PSYCOPG_NEW_BOOLEAN,HAVE_PQFREEMEM,HAVE_PQPROTOCOL3
rpath = ${database:location}/lib
include-dirs = ${database:location}/include
library-dirs = ${database:location}/lib
"""

class mysql( postgres ):
    dbi_module='mysql-python'
    parts ="""
[database]
recipe = zc.recipe.cmmi
url = http://mysql.mirrors.pair.com/Downloads/MySQL-5.0/mysql-5.0.51b.tar.gz

[database-ctl]
recipe = lovely.recipe:mkfile
path = ${buildout:bin-directory}/start-mysql
mode = 0755
content =
 #!/bin/sh
 {database:location}/bin/safe_mysqld $*

[database-shell]
recipe = lovely:recipe:mkfile
path = ${buildout:bin-directory}/mysql
mode = 0755
content =
 #!/bin/sh
 {database:location}/bin/mysql $*

[dbi-module]
recipe = zc.recipe.egg:custom
find-links = http://superb-west.dl.sourceforge.net/sourceforge/mysql-python/MySQL-python-1.2.2.tar.gz
rpath = ${database:location}/lib
include-dirs = ${database:location}/include
library-dirs = ${database:location}/lib
"""

kinds = { 'mysql':mysql,
          'postgres':postgres,
          'sqlite':sqlite3,
          'sqlite3':sqlite3,
          'postgresql':postgres}


