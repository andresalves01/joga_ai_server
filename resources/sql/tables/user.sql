SET search_path TO joga_ai;

CREATE TABLE IF NOT EXISTS user (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(320) UNIQUE NOT NULL,
  password VARCHAR(100),
  ssn CHAR(11) UNIQUE,
  phone_number CHAR(11) UNIQUE,
  profile_pic_url VARCHAR(2080),
  address_id INT,

  FOREIGN KEY (address_id) REFERENCES address (id) ON DELETE SET NULL ON UPDATE CASCADE,

  CHECK (email ~ '^[a-zA-Z][a-zA-Z0-9]*([._][a-zA-Z0-9]{1,})*@[a-zA-Z][a-zA-Z0-9]*([.-][a-zA-Z0-9]{1,}){1,}$'),
  CHECK (ssn ~ '^[0-9]{11}$'),
  CHECK (phone_number ~ '^[0-9]{11}$')
);