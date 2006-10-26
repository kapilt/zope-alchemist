"""
database access definition

$Id$
"""

from ore.alchemist.engine import get_engine

database = get_engine('mysql://root@localhost/orgperson', echo=True)
