
from ore.alchemist.engine import get_engine

database = get_engine('postgres://localhost/auditlog', encoding='utf-8', convert_unicode=True, echo=True )



