from Products.Alchemist.archetypes import dump_site

def plone2rdb( self, db_uri='zpgsql://database=plone'):
    dump_site( self, db_uri )

