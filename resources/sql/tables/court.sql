SET search_path TO joga_ai;

CREATE TABLE IF NOT EXISTS court (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  address_id INT,
  
  evaluation_sum INT DEFAULT 0 NOT NULL,
  evaluation_count INT DEFAULT 0 NOT NULL,
  rating DECIMAL(3, 2),

  FOREIGN KEY (address_id) REFERENCES address (id) ON DELETE SET NULL ON UPDATE CASCADE,

  CHECK (rating >= 1.0 AND rating <= 5.0)
);

CREATE INDEX IF NOT EXISTS court_name_index ON court (name);
CREATE INDEX IF NOT EXISTS court_rating_index ON court(rating);