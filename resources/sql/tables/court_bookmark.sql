SET search_path TO joga_ai;

CREATE TABLE IF NOT EXISTS court_bookmark (
  user_id INT NOT NULL,
  court_id INT NOT NULL,
  PRIMARY KEY (user_id, court_id),
  FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (court_id) REFERENCES court (id) ON DELETE CASCADE ON UPDATE CASCADE
);