SET search_path TO joga_ai;

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

CREATE OR REPLACE TRIGGER "canceled_booking_trigger"
AFTER UPDATE OF cancellation_datetime ON joga_ai.slot
FOR EACH ROW
EXECUTE FUNCTION replace_canceled_booking();