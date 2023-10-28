-- Create schema if not exists
CREATE SCHEMA IF NOT EXISTS joga_ai;

-- Set the schema as the current schema
SET
  search_path TO joga_ai;

-- Create the "Address" table
CREATE TABLE IF NOT EXISTS address (
  id SERIAL PRIMARY KEY,
  street VARCHAR(100) NOT NULL,
  number INT,
  zipcode VARCHAR(20) NOT NULL,
  complement VARCHAR(50),
  block VARCHAR(100),
  city_district VARCHAR(100),
  city VARCHAR(100) NOT NULL,
  state VARCHAR(100) NOT NULL,
  country VARCHAR(60) NOT NULL,
  latitude NUMERIC(9, 6),
  longitude NUMERIC(9, 6),

  CHECK(street ~ '^[a-zA-Z0-9]+([ ][a-zA-Z0-9]+)*$'),
  CHECK(number >= 0),
  CHECK (zipcode ~ '^[0-9]{8,20}$'),
  CHECK(complement ~ '^[a-zA-Z0-9]+([ ][a-zA-Z0-9]+)*$'),
  CHECK(block ~ '^[a-zA-Z0-9]+([ ][a-zA-Z0-9]+)*$'),
  CHECK(city_district ~ '^[a-zA-Z0-9]+([ ][a-zA-Z0-9]+)*$'),
  CHECK(city ~ '^[a-zA-Z0-9]+([ ][a-zA-Z0-9]+)*$'),
  CHECK(state ~ '^[a-zA-Z0-9]+([ ][a-zA-Z0-9]+)*$'),
  CHECK(country ~ '^[a-zA-Z]{2,}([ ][a-zA-Z]+)*$')
);

-- Create the composite index on "city," "state," and "country"
CREATE INDEX IF NOT EXISTS address_index ON address (country, state, city, city_district);
CREATE INDEX IF NOT EXISTS coordinates_index ON address (latitude, longitude);

-- Create the "User" table
CREATE TABLE IF NOT EXISTS "user" (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(320) UNIQUE NOT NULL,
  password VARCHAR(100),
  ssn CHAR(11) UNIQUE,
  phone_number CHAR(11) UNIQUE,
  profile_pic_url VARCHAR(2080),
  address_id INT,

  FOREIGN KEY (address_id) REFERENCES address (id) ON DELETE SET NULL ON UPDATE CASCADE,

  CHECK (name ~ '^[a-zA-Z]{2,}([ ][a-zA-Z]+)*$'),
  CHECK (email ~ '^[a-zA-Z][a-zA-Z0-9]*([._][a-zA-Z0-9]{1,})*@[a-zA-Z][a-zA-Z0-9]*([.-][a-zA-Z0-9]{1,}){1,}$'),
  CHECK (ssn ~ '^[0-9]{11}$'),
  CHECK (phone_number ~ '^[0-9]{11}$')
);

-- Create the "Court" table
CREATE TABLE IF NOT EXISTS court (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  player_qty INT,
  description VARCHAR(1000),
  modality VARCHAR(50),
  address_id INT,
  
  evaluation_sum INT DEFAULT 0 NOT NULL,
  evaluation_count INT DEFAULT 0 NOT NULL,
  rating DECIMAL(3, 2) DEFAULT 0.0 NOT NULL,

  FOREIGN KEY (address_id) REFERENCES address (id) ON DELETE SET NULL ON UPDATE CASCADE,

  CHECK (name ~ '^[a-zA-Z0-9]{2,}([ ][a-zA-Z0-9]+)*$'),
  CHECK(player_qty >= 2 AND player_qty <= 22)
);

CREATE INDEX IF NOT EXISTS court_name_index ON court (name);
CREATE INDEX IF NOT EXISTS court_player_qty_index ON court (player_qty);
CREATE INDEX IF NOT EXISTS court_modality_index ON court (modality);
CREATE INDEX IF NOT EXISTS court_rating_index ON court(rating);

-- Create the "CourtRating" table
CREATE TABLE IF NOT EXISTS court_rating (
  user_id INT,
  court_id INT NOT NULL,
  rating INT NOT NULL,
  comment VARCHAR(480),

  PRIMARY KEY (user_id, court_id),
  
  FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE SET NULL ON UPDATE CASCADE,
  FOREIGN KEY (court_id) REFERENCES court (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CHECK(rating > 0 AND rating <= 5)
);

-- Create the "Slot" table
CREATE TABLE IF NOT EXISTS slot (
  id SERIAL PRIMARY KEY,
  reservation_datetime TIMESTAMP,
  price DECIMAL(9, 2) NOT NULL,
  cancellation_datetime TIMESTAMP,
  user_id INT,
  court_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE SET NULL ON UPDATE CASCADE,
  FOREIGN KEY (court_id) REFERENCES court (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CHECK(price >= 0.0),
  CHECK(cancellation_datetime <= reservation_datetime)
);

CREATE INDEX IF NOT EXISTS slot_time_index ON slot (reservation_datetime);
CREATE INDEX IF NOT EXISTS slot_price_index ON slot (cancellation_datetime); 

CREATE UNIQUE INDEX IF NOT EXISTS unique_court_booking
ON slot (court_id, reservation_datetime)
WHERE cancellation_datetime IS NULL;

CREATE UNIQUE INDEX IF NOT EXISTS unique_user_booking
ON slot (user_id, reservation_datetime)
WHERE cancellation_datetime IS NULL;

CREATE TABLE IF NOT EXISTS amenity (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE,
  icon_url VARCHAR(2080),
  CHECK (name ~ '^[a-zA-Z]+$')
);

CREATE TABLE IF NOT EXISTS photo (
  id SERIAL PRIMARY KEY,
  url VARCHAR(2080),
  court_id INT NOT NULL,
  FOREIGN KEY (court_id) REFERENCES court (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS court_has_amenity (
  court_id INT NOT NULL,
  amenity_id INT NOT NULL,
  PRIMARY KEY (court_id, amenity_id),
  FOREIGN KEY (court_id) REFERENCES court (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (amenity_id) REFERENCES amenity (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS court_bookmark (
  user_id INT NOT NULL,
  court_id INT NOT NULL,
  PRIMARY KEY (user_id, court_id),
  FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (court_id) REFERENCES court (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- TODO: delete address if user or court is deleted