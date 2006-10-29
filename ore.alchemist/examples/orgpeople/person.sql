-- database definition 
create database orgperson;
connect orgperson;

create table Addresses (
  address_id       integer primary key auto_increment,
  name		   varchar(120) not null,
  address_1        varchar(120),
  address_2        varchar(120),
  city		   varchar(120),
  state		   varchar(2),
  zip		   varchar(9)
) ENGINE=INNODB;

create table Persons (
   person_id   	   integer primary key auto_increment,
   first_name 	   varchar(100) null,
   last_name	   varchar(100) null,
   email	   varchar(100) not null,
   phone_number    varchar(40)  null,
   address_id 	   integer,
   created	   date,
   foreign key ( address_id ) references Addresses( address_id ) on delete cascade
) ENGINE=INNODB;



