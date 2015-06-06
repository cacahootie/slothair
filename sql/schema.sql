DROP TABLE AIRPORTS;
DROP TABLE AIRLINES;
DROP TABLE ROUTES;

CREATE TABLE AIRPORTS
	(
		airport_id varchar, name varchar, city varchar, country varchar,
		iata_faa_id char(3), icao_id char(4), lat real, lng real,
		altitude varchar, tz_offset varchar, dst char(1), tz varchar
	);

CREATE TABLE AIRLINES
	(
		airline_id varchar, name varchar, alias varchar, iata_id char(3),
		icao_id char(5), callsign varchar, country varchar, active char(1)
	);

CREATE TABLE ROUTES
	(
		airline char(3), airline_id varchar, 
		source_iata char(3), source_id varchar,
		dest_iata char(3), dest_id varchar,
		codeshare char(1), stops integer,
		equipment varchar
	);