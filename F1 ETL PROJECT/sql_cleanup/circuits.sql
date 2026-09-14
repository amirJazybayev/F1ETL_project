create table circuits (
	circuit_reference text,
	circuit_name text,
	circuit_location text,
	circuit_country text,
	circuit_lat real,
	circuit_lng real,
	circuit_alt text,
	raceId int,
	year int,
	race_name text,
	race_date text,
	race_time text
)

select * from circuits

--dropping race_time column, due to most of its data being empty
alter table circuits
drop column race_time;

--eliminatting all '\N' values
update circuits 
set 
	circuit_alt = case when circuit_alt = '\N' then '0' else circuit_alt end,
	race_date = case when race_date = '\N' then '0' else race_date end,
	race_name = case when race_name = '\N' then '0' else race_name end;

--verifying changes
select * from circuits where
circuit_alt = '\N' and race_date = '\N' and race_name = '\N';

--changing circuit_alt's datatype 
alter table circuits
alter column circuit_alt type int 
using circuit_alt::int;

--casting datetime format for race_date column
alter table circuits
alter column race_date type date
using to_date (race_date, 'MM/DD/YYYY');

--creating final schema 
create table circuits_final (
	circuit_reference text,
	circuit_name text,
	circuit_location text,
	circuit_country text,
	circuit_lat decimal(5,2),
	circuit_lng decimal(5,2),
	circuit_alt int,
	raceId int,
	year int,
	race_name text,
	race_date date
);

--verifying 
select * from circuits_final

--convert and copy the data from circuits
insert into circuits_final (circuit_reference, circuit_name, circuit_location,
circuit_country, circuit_lat, circuit_lng, circuit_alt, raceId, year, race_name,
race_date)
select
	circuit_reference,
	circuit_name,
	circuit_location,
	circuit_country,
	circuit_lat::decimal(5,2),
	circuit_lng::decimal(5,2),
	circuit_alt,
	raceId,
	year,
	race_name,
	race_date
from circuits;

--verifying
select * from circuits_final where
circuit_reference is null or circuit_name is null or circuit_location is null or
circuit_country is null or circuit_lat is null or circuit_lng is null or
circuit_alt is null or raceId is null or year is null or race_name is null or
race_date is null 
limit 10;

--adding additional division into different technical regulations eras
/*
reason: demonstrating changes in teams and drivers performance after each major
technical reagulation change can help to analyze and gain deeper understanding 
of what causes each team to succeed or struggle
*/
create table regs_eras (
	era_id serial primary key,
	era_name text,
	era_code text,
	start_year int,
	end_year int,
	description text
);

insert into regs_eras (era_name, era_code, start_year, end_year, description)
values
('Early F1', 'reg1', 1950, 1960, 'The beggining of F1, few safety and technial reggulations'),
('New Engine formula', 'reg2', 1961, 1982, 'Engine capacity cut down to 1.5l, minimum car weight of 450kg introduced'),
('Flat-bottomed cars', 'regs3', 1983, 1988, 'Banning "ground effect" in favour of flat-bottom floor regulations, affecting aerodynamic performance of the cars'),
('Turbo engines ban', 'regs4', 1989, 1993, 'Banning turbocharged cars'),
('Ban on driver aids', 'regs5', 1994, 1997, 'Banning all electronic driver aid devies, such as active suspension, traction control, anti-lock braking etc.'),
('Narrower cars, grooved tyres', 'regs6', 1998, 2008, 'Car widths reduced from two metres to 1.8m, while grooved tyres were also introduced (three on the front, four on the rear) to get spiralling speeds under control'),
('Aerodynamics overhaul', 'regs7', 2009, 2013, 'Majority of of all aerodynamic devices were banned, driver-adjustable front wings were permitted, slick tyres were re-introduced, engine regulation change to 2.4-litre naturally aspirated V8s.'),
('Turbo-hybrid power units', 'regs8', 2014, 2016, 'Introduction of 1.6-litre V6 turbo hybrid power units'),
('Longer, wider and faster cars', 'regs9', 2017, 2021, 'Increasing car widths up to 2m, front wing widths and the minimum overall weight');

--verifying
select * from regs_eras

--reducing redundancy and creating a final circuits table 
drop table if exists circuits_final;
create table circuits_final (
	circuit_id serial primary key,
	circuit_reference varchar(50) not null unique,
	circuit_name varchar(50) not null,
	circuit_location varchar(100),
	circuit_country varchar(100),
	circuit_lat decimal (5,2),
	circuit_lng decimal (5,2),
	circuit_alt int
)

insert into circuits_final (circuit_reference, circuit_name, circuit_location, circuit_country, circuit_lat, circuit_lng, circuit_alt)
select distinct
	circuit_reference::varchar(50),
	circuit_name::varchar(50),
	circuit_location::varchar(100),
	circuit_country::varchar(100),
	circuit_lat::decimal(5,2),
	circuit_lng::decimal(5,2),
	circuit_alt
from circuits;

--verifying changes
select * from circuits_final

select distinct circuit_reference from circuits

--creating a table for distinct data of all races, including year, name, location, winning driver etc.

--raceid is a good candidate key, verifying that it has no duplicates
select raceid, count(*) from circuits
group by raceid having count(*)>1;

--creating a table
drop table if exists circuit_races; 
create table circuit_races (
	raceid int primary key,
	circuit_reference varchar(50) references circuits_final(circuit_reference),
	year int,
	race_name varchar(100),
	race_date date
);

insert into circuit_races (raceid, circuit_reference, year, race_name, race_date)
select 
	raceid,
	circuit_reference::varchar(50),
	year,
	race_name::varchar(100),
	race_date
from circuits;

--verifying 
select * from circuit_races
order by raceid asc;

--dropping original table
drop table circuits

insert into regs_eras (era_name, era_code, start_year, end_year, description)
values 
('New "ground effect" era', 'regs10', 2022, 2025, 'Re-introduction of the "ground effect" regulations and new aerodynamic rules')