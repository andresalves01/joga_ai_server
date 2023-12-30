SET search_path TO joga_ai;

CREATE OR REPLACE FUNCTION prevent_new_evaluation()
RETURNS TRIGGER AS $$
BEGIN
  RAISE NOTICE 'Fields evaluation_sum, evaluation_count and rating initializated with default values.';
  NEW.evaluation_sum := 0;
  NEW.evaluation_count := 0;
  NEW.rating := NULL;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER prevent_new_evaluation
BEFORE INSERT ON court
FOR EACH ROW
EXECUTE FUNCTION prevent_new_evaluation();

CREATE OR REPLACE FUNCTION prevent_direct_rating_update()
RETURNS TRIGGER AS $$
BEGIN
  IF pg_trigger_depth() <= 1 THEN
    RAISE NOTICE 'Is not possible to directly change evaluation_sum, evaluation_count or rating';
    NEW.evaluation_sum := OLD.evaluation_sum;
    NEW.evaluation_count := OLD.evaluation_count;
    NEW.rating := OLD.rating;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER prevent_direct_rating_update_trigger
BEFORE UPDATE ON court
FOR EACH ROW
EXECUTE FUNCTION prevent_direct_rating_update();

CREATE TRIGGER automatic_address_deletion_trigger_court
AFTER DELETE ON court
FOR EACH ROW
EXECUTE FUNCTION automatic_address_deletion();