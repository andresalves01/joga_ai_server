SET search_path TO joga_ai;

CREATE OR REPLACE FUNCTION update_full_text_search()
RETURNS TRIGGER AS $$
BEGIN
  NEW.full_text_search := setweight(to_tsvector('english', NEW.city), 'A') ||
                          setweight(to_tsvector('english', COALESCE(NEW.city_district, '')), 'B') ||
                          setweight(to_tsvector('english', COALESCE(NEW.neighborhood, '')), 'B') ||
                          setweight(to_tsvector('english', NEW.state_code), 'C') ||
                          setweight(to_tsvector('english', NEW.state), 'C') ||
                          setweight(to_tsvector('english', NEW.country_code), 'D') ||
                          setweight(to_tsvector('english', NEW.country), 'D') ||
                          setweight(to_tsvector('english', COALESCE(NEW.county, '')), 'E') ||
                          to_tsvector('english', NEW.street || ' ' ||
                                              COALESCE(NEW.number || ' ', '') ||
                                              NEW.zipcode || ' ' ||
                                              COALESCE(NEW.complement || ' ', '')) ||
                                              COALESCE(NEW.city_district || ' ', '') ||
                                              COALESCE(NEW.neighborhood || ' ', '') ||
                                              COALESCE(NEW.state_code || ' ', '') ||
                                              COALESCE(NEW.state || ' ', '') ||
                                              COALESCE(NEW.country_code || ' ', '') ||
                                              COALESCE(NEW.country || ' ', '') ||
                                              COALESCE(NEW.county || ' ', '');

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_full_text_search_trigger
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

CREATE TRIGGER automatic_address_deletion_trigger
AFTER DELETE ON user OR court
FOR EACH ROW
EXECUTE FUNCTION automatic_address_deletion();
