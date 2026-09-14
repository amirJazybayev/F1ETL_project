create table drivers (
	driver_ref text,
	driver_number text,
	driver_code text,
	driver_forename text,
	driver_surname text,
	driver_dob text,
	driver_nationality text,
	result_id INT,
	race_id INT,
	result_number INT,
	start_pos INT,
	final_pos text,
	final_pos_text text,
	points INT,
	fastets_lap_no text,
	rank text,
	fastest_lap text,
	fastest_lap_speed text,
	status text	
)

drop table drivers;

create table drivers (
	driverRef text,
	driver_number text,
	driver_code text,
	driver_forename text,
	driver_surname text,
	driver_dob text,
	driver_nationality text,
	resultId INT,
	raceId INT,
	result_number INT,
	start_position INT,
	final_position text,
	positionText text,
	positionOrder text,
	points INT,
	fastestLap text,
	rank text,
	fastestLapTime text,
	fastestLapSpeed text,
	status text	
)

alter table drivers
alter column points type text;

select * from drivers

--eliminating '\N' values from final position column
update drivers 
set final_position = 0 where final_position = '\N';

--verifying 
select final_position from drivers
where final_position = '\N';

--checking which possible text values can position order column hold
select distinct positiontext, positionorder from drivers where
positionText !~ '^\d+$';

--eliminating '\N' values from driver number column and swapping it to 0, since number 0 is illegal on the car
update drivers 
set driver_number = 0 where driver_number = '\N';

--eliminating '\N' values from fastest lap, rank, fastestlaptime, fastestlapspeed column and swapping it to 0
update drivers 
set 
	fastestlap = case when fastestlap = '\N' then '0' else fastestlap end,
	rank = case when rank = '\N' then '0' else rank end,
	fastestlaptime = case when fastestlaptime = '\N' then '0' else fastestlaptime end,
	fastestlapspeed = case when fastestlapspeed = '\N' then '0' else fastestlapspeed end;

--verifying
select fastestlap from drivers
where fastestlap = '\N';


--creating drivers table 
drop table if exists drivers_final;
create table drivers_final(
	driver_id serial primary key,
	driver_ref varchar(50) not null unique,
	driver_number int,
	driver_code varchar(5),
	driver_firstname varchar(100),
	driver_lastname varchar(100),
	driver_dob date,
	driver_nationality varchar(100)
);

-- checking different regex patterns
select distinct driver_dob, length(driver_dob)
from drivers
where driver_dob !~ '^\d{4}-\d{2}-\d{2}$'
  and driver_dob !~ '^\d{2}/\d{2}/\d{4}$'
  and driver_dob != '\N'
  and driver_dob is not null
order by driver_dob;

insert into drivers_final (driver_ref, driver_number, driver_code, driver_firstname, driver_lastname, driver_dob, driver_nationality)
select distinct
	driverref::varchar(50),
	driver_number::int,
	driver_code::varchar(5),
	driver_forename::varchar(100),
	driver_surname::varchar(50),
	TO_DATE( 
		driver_dob,
		case
			when driver_dob ~ '^\d{4}-\d{2}-\d{2}$' then 'YYYY-MM-DD'  
        	when driver_dob ~ '^\d{2}/\d{2}/\d{4}$' then 'MM/DD/YYYY'
			when driver_dob ~ '^\d{1}/\d{2}/\d{4}$' then 'MM/DD/YYYY'
			when driver_dob ~ '^\d{2}/\d{1}/\d{4}$' then 'DD/MM/YYYY'
			when driver_dob ~ '^\d{1}/\d{1}/\d{4}$' then 'DD/MM/YYYY'
		end
	),
	driver_nationality::varchar(100)
from drivers;

--verifying
select * from drivers_final

--checking different regex patterns for the fastest lap
select distinct fastestlaptime
from drivers
where fastestlaptime != '\N'
  and fastestlaptime !~ '^\d+:\d{2}\.\d+$'
  and fastestlaptime !~ '^\d+\.\d+$'
order by fastestlaptime;

--creating table for drivers' race data
drop table if exists drivers_race;
create table drivers_race (
	result_id int primary key,
	race_id int references circuit_races(raceid),
	driver_id int references drivers_final(driver_id),
	result_driver_num int,
	start_position int,
	final_position int,
	position_text varchar(50),
	position_order varchar(50),
	points decimal(3,1),
	fastest_lap_time interval,
	fastest_lap_speed decimal (5,2),
	status varchar(50)
);

insert into drivers_race(result_id, race_id, driver_id, result_driver_num, start_position, final_position, position_text, position_order, 
points, fastest_lap_time, fastest_lap_speed, status)
select
	dr.resultid,
	dr.raceid,
	df.driver_id,
	dr.result_number,
	dr.start_position,
	dr.final_position::int,
	dr.positiontext::varchar(50),
	dr.positionorder::varchar(50),
	dr.points::decimal(3,1),
	case
        when nullif(dr.fastestLapTime, '\N') is null then null
        when dr.fastestLapTime ~ '^\d+:\d{2}\.\d+$'
            then TO_NUMBER(SPLIT_PART(dr.fastestlaptime, ':', 1), '99') * interval '1 minute' + TO_NUMBER(SPLIT_PART(dr.fastestlaptime, ':', 2), '99.999') * interval '1 second'
        when dr.fastestlaptime ~ '^\d+\.\d+$'
            then dr.fastestlaptime::numeric * interval '1 second'
        else null
    end,
	dr.fastestlapspeed::decimal(5,2),
	dr.status::varchar(50)
from drivers dr
join drivers_final df on dr.driverref=df.driver_ref;

--verifying
select * from drivers_race

--casting int to position_final
alter table drivers_race
alter column position_order type int
using position_order::int;

--dropping original table
drop table drivers