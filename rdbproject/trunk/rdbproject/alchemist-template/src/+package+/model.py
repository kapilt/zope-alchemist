import sqlalchemy as rdb
#from elixir import Entity, Field, OneToOne, ManyToMany, ManyToOne, OneToMany, options_defaults
#from sqlalchemy import String, Date, Boolean, Integer, Float

__all__ = []

options_defaults.update({
    'inheritance' : 'multi',
    'shortnames': True,
#    'table_options' : {'mysql_engine':'InnoDB'},
    })


class Users( object ):

    def checkPassword( self, *args, **kw):
        return True

