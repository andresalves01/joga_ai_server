SET search_path TO joga_ai;

CREATE TABLE IF NOT EXISTS photo (
  id SERIAL PRIMARY KEY,
  url VARCHAR(2080),
  presentation_order INT NOT NULL,
  court_id INT NOT NULL,
  FOREIGN KEY (court_id) REFERENCES court (id) ON DELETE CASCADE ON UPDATE CASCADE
);