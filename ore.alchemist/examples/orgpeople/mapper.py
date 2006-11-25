"""

Map Domain classes to domain model


"""

from sqlalchemy import mapper, relation, backref
from ore.alchemist.mapper import bind_mapper

import schema as app_schema
import domain as app_model

address_mapper = bind_mapper( app_model.Address, app_schema.AddressTable )

person_mapper = bind_mapper( app_model.Person,
                             app_schema.PersonTable,
                             properties={ 'address' :
                                          relation( address_mapper,
                                                    lazy=True,
                                                    backref=backref('person', uselist=False))
                                          }
                             )



