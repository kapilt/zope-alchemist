-- database definition 
create database if not exists orgperson character set utf8;
connect orgperson;


create table if not exists Addresses (
  address_id       integer primary key auto_increment,
  name		   varchar(120) not null,
  address_1        varchar(120),
  address_2        varchar(120),
  city		   varchar(120),
  state		   varchar(2),
  zip		   varchar(9)
) ENGINE=INNODB;

create table if not exists Persons (
   person_id   	   integer primary key auto_increment,
   first_name 	   varchar(100) null,
   last_name	   varchar(100) null,
   email	   varchar(100) not null,
   phone_number    varchar(40)  null,
   address_id 	   integer,
   created	   date,
   foreign key ( address_id ) references Addresses( address_id ) on delete cascade
) ENGINE=INNODB;

create table if not exists States (
   state_code      varchar( 2 ) primary key,
   state_name	   varchar( 120 )
);

-- just a few states where i've lived ;-)
insert into States values ( "VA", "Virginia");
insert into States values ( "CA", "California");
insert into States values ( "KS", "Kansas");
insert into States values ( "NY", "New York");
insert into States values ( "NJ", "New Jersey");
insert into States values ( "MA", "Massachussets");
insert into States values ( "UT", "Utah");
insert into States values ( "IL", "Illinois");
insert into States values ( "CT", "Connecticut");

     
 
