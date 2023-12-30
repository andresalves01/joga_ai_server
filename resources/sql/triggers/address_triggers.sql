SET search_path TO joga_ai;

CREATE OR REPLACE FUNCTION update_full_text_search()
RETURNS TRIGGER AS $$
BEGIN
  NEW.full_text_search := setweight(to_tsvector('portuguese', NEW.city), 'A') ||
                          setweight(to_tsvector('portuguese', COALESCE(NEW.city_district, '')), 'A') ||
                          setweight(to_tsvector('portuguese', COALESCE(NEW.neighborhood, '')), 'A') ||
                          setweight(to_tsvector('portuguese', NEW.state_code), 'B') ||
                          setweight(to_tsvector('portuguese', NEW.state), 'B') ||
                          setweight(to_tsvector('portuguese', NEW.country_code), 'C') ||
                          setweight(to_tsvector('portuguese', NEW.country), 'C') ||
                          setweight(to_tsvector('portuguese', NEW.street), 'D') ||
                          setweight(to_tsvector('portuguese', NEW.number), 'D') ||
                          setweight(to_tsvector('portuguese', NEW.zipcode), 'D');

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER update_full_text_search_trigger
BEFORE INSERT OR UPDATE
ON address
FOR EACH ROW
EXECUTE FUNCTION update_full_text_search();

CREATE OR REPLACE FUNCTION automatic_address_deletion()
RETURNS TRIGGER AS $$
BEGIN
  DELETE FROM address WHERE id = OLD.address_id;
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

