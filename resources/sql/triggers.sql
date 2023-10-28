-- Create a trigger function
CREATE OR REPLACE FUNCTION replace_canceled_booking()
RETURNS TRIGGER AS $$
BEGIN
  IF OLD.user_id IS NOT NULL AND NEW.cancellation_datetime IS NOT NULL AND OLD.cancellation_datetime IS NULL THEN
    INSERT INTO joga_ai.slot (reservation_datetime, price, user_id, court_id, cancellation_datetime)
    VALUES (OLD.reservation_datetime, OLD.price, NULL, OLD.court_id, NULL);
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger to activate the function when slotCancellationDate is updated
CREATE OR REPLACE TRIGGER "canceled_booking_trigger"
AFTER UPDATE OF cancellation_datetime ON joga_ai.slot
FOR EACH ROW
EXECUTE FUNCTION replace_canceled_booking();

-- Create a trigger function
CREATE OR REPLACE FUNCTION prevent_new_evaluation()
RETURNS TRIGGER AS $$
BEGIN
  IF (TG_OP = 'INSERT') THEN
    RAISE NOTICE 'Fields evaluation_sum, evaluation_count and rating set to zero';
    NEW.evaluation_sum := 0;
    NEW.evaluation_count := 0;
    NEW.rating := 0;
  ELSIF pg_trigger_depth() <= 1 THEN
    RAISE NOTICE 'Is not possible to directly change evaluation_sum, evaluation_count or rating';
    NEW.evaluation_sum := OLD.evaluation_sum;
    NEW.evaluation_count := OLD.evaluation_count;
    NEW.rating := OLD.rating;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger to activate the function when slotCancellationDate is updated
CREATE OR REPLACE TRIGGER prevent_new_evaluation
BEFORE INSERT OR UPDATE ON joga_ai.court
FOR EACH ROW
EXECUTE FUNCTION prevent_new_evaluation();

-- Create a trigger to activate the function when slotCancellationDate is updated
CREATE OR REPLACE FUNCTION update_rating()
RETURNS TRIGGER AS $$
BEGIN
  IF (TG_OP = 'INSERT') THEN
    UPDATE joga_ai.court
    SET evaluation_count = evaluation_count + 1,
        evaluation_sum = evaluation_sum + NEW.rating,
        rating = (evaluation_sum + NEW.rating) / (evaluation_count + 1)
    WHERE id = NEW.court_id;
    RETURN NEW;
  ELSIF (TG_OP = 'UPDATE') THEN
    UPDATE joga_ai.court
    SET evaluation_sum = evaluation_sum + NEW.rating - OLD.rating,
        rating = (evaluation_sum + NEW.rating - OLD.rating) / evaluation_count
    WHERE id = NEW.court_id;
    RETURN NEW;
  ELSIF (TG_OP = 'DELETE') THEN
    UPDATE joga_ai.court
    SET evaluation_count = evaluation_count - 1,
        evaluation_sum = evaluation_sum - OLD.rating,
        rating = (evaluation_sum - OLD.rating) / (evaluation_count - 1)
    WHERE id = OLD.court_id AND evaluation_count > 1;

    UPDATE joga_ai.court
    SET evaluation_count = 0,
        evaluation_sum = 0,
        rating = 0.0
    WHERE id = OLD.court_id AND evaluation_count <= 1;
    RETURN OLD;
  END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER update_rating
AFTER INSERT OR UPDATE OR DELETE ON joga_ai.court_rating
FOR EACH ROW
EXECUTE FUNCTION update_rating();


-- Create a function that checks for future reservations
CREATE OR REPLACE FUNCTION check_user_slot_reservation()
RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM joga_ai.slot
    WHERE user_id = OLD.id
      AND reservation_datetime > NOW()
      AND cancellation_datetime IS NULL
  ) THEN
    RAISE EXCEPTION 'Cannot delete user with future slot reservations';
  END IF;
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger that calls the function before DELETE operation on the user table
CREATE OR REPLACE TRIGGER prevent_user_deletion
BEFORE DELETE ON "user"
FOR EACH ROW
EXECUTE FUNCTION check_user_slot_reservation();

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
    RAISE EXCEPTION "Cannot evaluate court if user does not have a previous and not cancelled slot reservation on that court";
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER allow_court_rating
BEFORE INSERT ON court_rating
FOR EACH ROW
EXECUTE FUNCTION check_court_rating()