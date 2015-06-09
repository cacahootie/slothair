DROP MATERIALIZED VIEW IF EXISTS ROUTES_PER_AIRPORT;
DROP MATERIALIZED VIEW IF EXISTS INTERNATIONAL_ROUTES_PER_AIRPORT;
DROP MATERIALIZED VIEW IF EXISTS INTERNATIONAL_ROUTES;
DROP TABLE IF EXISTS AIRPORTS;
DROP TABLE IF EXISTS AIRLINES;
DROP TABLE IF EXISTS ROUTES;

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

CREATE MATERIALIZED VIEW INTERNATIONAL_ROUTES
AS
	SELECT source_id, dest_id
	FROM ROUTES
	JOIN AIRPORTS src_ap
		ON ROUTES.source_id = src_ap.airport_id
	JOIN AIRPORTS dst_ap
		ON ROUTES.dest_id = dst_ap.airport_id
	WHERE
		src_ap.country != dst_ap.country;

CREATE MATERIALIZED VIEW INTERNATIONAL_ROUTES_PER_AIRPORT
AS
	SELECT
		source_id as source_id,
		COUNT(dest_id) AS num_routes
	FROM INTERNATIONAL_ROUTES
	GROUP BY source_id;

CREATE MATERIALIZED VIEW ROUTES_PER_AIRPORT
AS
	SELECT
		source_id as source_id,
		COUNT(dest_id) AS num_routes
	FROM ROUTES
	GROUP BY source_id;
