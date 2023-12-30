CREATE SCHEMA IF NOT EXISTS joga_ai;
SET search_path TO joga_ai;

CREATE TABLE IF NOT EXISTS address (
  id SERIAL PRIMARY KEY NOT NULL,

  street VARCHAR(100) NOT NULL,
  number VARCHAR(10),

  zipcode VARCHAR(20) NOT NULL,
  complement VARCHAR(30),
  neighborhood VARCHAR(30),

  city_district VARCHAR(60),
  city VARCHAR(60) NOT NULL,

  county VARCHAR(30), -- Ex: Região Metropolitana de Belo Horizonte, Vale do Aço, etc.

  state VARCHAR(60) NOT NULL,
  state_code VARCHAR(3) NOT NULL,

  country VARCHAR(60) NOT NULL,
  country_code CHAR(2) NOT NULL,

  full_text_search tsvector,

  latitude NUMERIC(9, 6),
  longitude NUMERIC(9, 6)
);

CREATE INDEX IF NOT EXISTS county_index ON address (county, state);

CREATE INDEX IF NOT EXISTS city_state_index ON address (city, state);
CREATE INDEX IF NOT EXISTS city_district_index ON address (city_district, city, state);
CREATE INDEX IF NOT EXISTS neighborhood_index ON address (neighborhood, city, state);

CREATE INDEX IF NOT EXISTS city_index ON address (city);
CREATE INDEX IF NOT EXISTS state_index ON address (state);
CREATE INDEX IF NOT EXISTS country_index ON address (country);

CREATE INDEX IF NOT EXISTS full_text_index ON address USING gin(full_text_search);
CREATE INDEX IF NOT EXISTS coordinates_index ON address USING gist (point(latitude, longitude));