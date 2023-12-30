SET search_path TO joga_ai;

CREATE TABLE IF NOT EXISTS slot (
  id SERIAL PRIMARY KEY,
  reservation_datetime TIMESTAMPTZ NOT NULL,
  price DECIMAL(9, 2) NOT NULL,
  cancellation_datetime TIMESTAMPTZ,
  user_id INT,
  court_id INT,

  FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE SET NULL ON UPDATE CASCADE,
  FOREIGN KEY (court_id) REFERENCES court (id) ON DELETE SET NULL ON UPDATE CASCADE,

  CHECK(price >= 50.0),
  CHECK(cancellation_datetime <= reservation_datetime)
);

CREATE INDEX IF NOT EXISTS slot_datetime_index ON slot (reservation_datetime);
CREATE INDEX IF NOT EXISTS slot_price_index ON slot (price); 

CREATE UNIQUE INDEX IF NOT EXISTS unique_court_booking
ON slot (court_id, reservation_datetime)
WHERE cancellation_datetime IS NULL;

CREATE UNIQUE INDEX IF NOT EXISTS unique_user_booking
ON slot (user_id, reservation_datetime)
WHERE cancellation_datetime IS NULL;