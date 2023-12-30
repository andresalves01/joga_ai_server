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

  county VARCHAR(120), -- Ex: Região Metropolitana de Belo Horizonte, Vale do Aço, etc.

  state VARCHAR(60) NOT NULL,
  state_code VARCHAR(3) NOT NULL,

  country VARCHAR(60) NOT NULL,
  country_code CHAR(2) NOT NULL,

  full_text_search tsvector,

  latitude NUMERIC(9, 6),
  longitude NUMERIC(9, 6)
);

-- First, select all cities at the same county as the searcher
CREATE INDEX IF NOT EXISTS county_index ON address USING hash (county, state);

-- If the user clicks on the city, then search parameters should prioritize results within that city
CREATE INDEX IF NOT EXISTS city_district_index ON address (city_district text_pattern_ops, city, state);
CREATE INDEX IF NOT EXISTS neighborhood_index ON address (neighborhood text_pattern_ops, city, state);

-- If none result until now matched, try to match with other parameters
CREATE INDEX IF NOT EXISTS city_index ON address (city text_pattern_ops);
CREATE INDEX IF NOT EXISTS state_index ON address (state text_pattern_ops);
CREATE INDEX IF NOT EXISTS country_index ON address (country text_pattern_ops);

-- Lastly, try to match the whole address
CREATE INDEX IF NOT EXISTS full_text_index ON address USING gin(full_text_search);

-- For geospacial searches
CREATE INDEX IF NOT EXISTS coordinates_index ON address USING gist (point(latitude, longitude));