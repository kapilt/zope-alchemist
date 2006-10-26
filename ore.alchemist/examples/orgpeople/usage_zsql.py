
"""
using zsql methods

separate methods for update, codebase littered with value manipulation and argument passing to
methods. optionally varying args and using conditional dtml syntax or creating lots of of little
utility zsql methods for various scenarios.

the numbers of methods tend to expand a great as the complexity of the model goes. 
"""

create_person.zsql

insert into persons(
    <dtml-if first_name>
      first_name,
    </dtml-if>
    <dtml-if last_name>
      last_name,
    </dtml-if>
    email
    ) values (
    <dtml-if first_name>
      <dtml-sqlvar first_name type="string">,
    </dtml-if>
    </dtml-if last_name>
      <dtml-sqlvar last_name type="string">,
    </dtml-if>
     <dtml-sqlvar email type="string">
    )

<dtml-comment>
arguments: first_name, 
title:Indicators Table Insert
connection_id:db_conn_cap_cpi
</dtml-comment>

edit_person.zsql

update persons
where 

delete_person.zsql


