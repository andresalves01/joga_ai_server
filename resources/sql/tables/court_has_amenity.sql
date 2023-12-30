SET search_path TO joga_ai;

CREATE TABLE IF NOT EXISTS court_has_amenity (
  court_id INT NOT NULL,
  amenity_id INT NOT NULL,
  PRIMARY KEY (court_id, amenity_id),
  FOREIGN KEY (court_id) REFERENCES court (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (amenity_id) REFERENCES amenity (id) ON DELETE CASCADE ON UPDATE CASCADE
);