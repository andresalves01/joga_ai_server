SET search_path TO joga_ai;

CREATE TABLE IF NOT EXISTS court_rating (
  user_id INT,
  court_id INT NOT NULL,
  rating INT NOT NULL,
  comment TEXT,
  
  FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (court_id) REFERENCES court (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CHECK(rating >= 1 AND rating <= 5)
);