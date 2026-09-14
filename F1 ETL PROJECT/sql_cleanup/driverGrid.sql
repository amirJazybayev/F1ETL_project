create table driverGrid (
	raceId int,
	driverId int,
	points int,
	position int,
	wins int
)

alter table driverGrid
alter column points type float;

select * from drivergrid

--creating a new table
drop table if exists driver_grid_final;
create table driver_grid_final(
	race_id int references circuit_races(raceid),
	driver_id int references drivers_final(driver_id),
	points decimal(6,1),
	position int,
	wins int
)

--need to swap driver id's
--checking if values between driver_grid and driver_race line up
select dg.raceid, dg.driverid, dg.position, dr.driver_id, dr.position_order from drivergrid dg
join drivers_race dr 
    on dg.raceid = dr.race_id 
    and dg.position = dr.position_order
limit 50;

--inserting values
insert into driver_grid_final (race_id, driver_id, points, position, wins)
select
	dg.raceid,
	dr.driver_id,
	dg.points::decimal(6,1),
	dg.position, 
	dg.wins
from drivergrid dg
join drivers_race dr on dg.raceid = dr.race_id and
dg.position = dr.position_order;

--verifying 
select*from driver_grid_final;

--dropping original table
drop table drivergrid