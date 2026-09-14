create table constructors (
	constructor_ref text,
	constructor_name text,
	constructor_nationality text,
	constructorStandingsId int,
	raceId int,
	constructor_points int,
	constructor_position int,
	postionText text,
	wins int
)

--changing constructor points to type float
alter table constructors
alter column constructor_points type float;
select * from constructors

--renaming columns
alter table constructors 
rename column constructorStandingsId to constructor_standings_id;
alter table constructors
rename column raceId to race_id;
alter table constructors
rename column postionText to position_text;

--verifying changes
select * from constructors

--eliminating 'E' (excluded) from position_text to normalize the table
alter table constructors
add column is_excluded boolean default false;
update constructors
set is_excluded = true where position_text = 'E';

--verifying changes
select constructor_standings_id from constructors where
is_excluded = true;

--creating a dimensional table to split constructor_ref and constructor_name
--since they identify the same teams
create table constructors_dim (
	constructor_ref varchar(50) primary key,
	constructor_name varchar(100) not null,
	constructor_nationality varchar(50)
);

insert into constructors_dim (constructor_ref, constructor_name, constructor_nationality)
select distinct
	constructor_ref::varchar(50),
	constructor_name::varchar(100),
	constructor_nationality::varchar(50)
from constructors;

--verifying changes
select * from constructors_dim

create table constructors_final (
	constructor_standings_id int primary key,
	constructor_ref varchar(50) references constructors_dim(constructor_ref),
	race_id int, --REFERENCE THIS
	constructor_points decimal(5,1),
	constructor_position int,
	position_text varchar(50),
	wins int, 
	is_excluded boolean
);

insert into constructors_final (constructor_standings_id, constructor_ref,
race_id, constructor_points, constructor_position, position_text, wins, is_excluded)
select
	constructor_standings_id,
	constructor_ref::varchar(50),
	race_id,
	constructor_points::decimal(5,1),
	constructor_position,
	position_text::varchar(50),
	wins,
	is_excluded
from constructors;	

--verifying changes
select * from constructors_final

/*



*/
--constructors schema needs to be restructurized in order to apply more constraints and dependencies
drop table if exists constructors_final;
drop table if exists constructors_dim;

create table constructors_final(
	contructor_id serial primary key,
	constructor_ref varchar(50) not null,
	constructor_name varchar(100) not null,
	constructor_nationality varchar(50)
)

insert into constructors_final (constructor_ref, constructor_name, constructor_nationality)
select distinct
	constructor_ref:: varchar(50),
	constructor_name:: varchar(100),
	constructor_nationality::varchar(100)
from constructors;

--verifying
select * from constructors_final

--fixing a gramatical error
alter table constructors_final
rename column contructor_id to constructor_id;

--creating a table to store all race data for each team

--verifying constructor_standings_id for a primary key role
select constructor_standings_id, count(*) from constructors
group by constructor_standings_id having count(*)>1;

create table constructor_races (
	constructor_standings_id int primary key,
	constructor_id int references constructors_final(constructor_id),
	race_id int references circuit_races(raceid),
	constructor_points decimal(6,1),
	constructor_position int,
	position_text varchar(50),
	wins int,
	is_excluded boolean
)

insert into constructor_races (constructor_standings_id, constructor_id, race_id, constructor_points, constructor_position,
position_text, wins, is_excluded)
select
	c.constructor_standings_id,
	cf.constructor_id, 
	c.race_id,
	c.constructor_points::decimal(6,1),
	c.constructor_position,
	c.position_text::varchar(50),
	c.wins,
	c.is_excluded
from constructors c
join constructors_final cf on c.constructor_ref = cf.constructor_ref;

--verifying
select*from constructor_races

--dropping original table
drop table constructors