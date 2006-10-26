"""

Map Domain classes to domain model


"""

from sqlalchemy import mapper
from ore.alchemist.mapper import bind_mapper

import schema as app_schema
import domain as app_model


person_mapper = bind_mapper( app_model.Person, app_schema.PersonTable )

address_mapper = bind_mapper( app_model.Address, app_schema.AddressTable )


