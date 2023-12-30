SET search_path TO joga_ai;

CREATE OR REPLACE FUNCTION check_court_rating()
RETURNS TRIGGER AS $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM joga_ai.slot
    WHERE user_id = NEW.user_id
      AND court_id = NEW.court_id
      AND cancellation_datetime IS NULL
      AND NOW() > reservation_datetime
  ) THEN
    RAISE EXCEPTION 'Cannot evaluate court if user does not have a previous and not cancelled slot reservation on that court';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER check_court_rating_trigger
BEFORE INSERT OR UPDATE ON court_rating
FOR EACH ROW
EXECUTE FUNCTION check_court_rating()


CREATE OR REPLACE FUNCTION new_court_evaluation()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE court
  SET evaluation_count = evaluation_count + 1,
      evaluation_sum = evaluation_sum + NEW.rating,
      rating = (evaluation_sum + NEW.rating) / (evaluation_count + 1)
  WHERE id = NEW.court_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER new_court_evaluation_trigger
AFTER INSERT ON court_rating
FOR EACH ROW
EXECUTE FUNCTION insert_new_court_evaluation();

CREATE OR REPLACE FUNCTION delete_court_evaluation()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE court
  SET evaluation_count = evaluation_count - 1,
      evaluation_sum = evaluation_sum - OLD.rating,
      rating = CASE WHEN evaluation_count > 1 THEN (evaluation_sum - OLD.rating) / (evaluation_count - 1)
                    ELSE NULL
               END
  WHERE id = OLD.court_id;

  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER delete_court_evaluation_trigger
AFTER DELETE ON court_rating
FOR EACH ROW
EXECUTE FUNCTION delete_court_evaluation();

CREATE OR REPLACE FUNCTION update_court_evaluation()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM delete_court_evaluation();
  PERFORM insert_new_court_evaluation();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_court_evaluation_trigger
AFTER UPDATE ON court_rating
FOR EACH ROW
EXECUTE FUNCTION update_court_evaluation();
