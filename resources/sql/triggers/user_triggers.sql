SET search_path TO joga_ai;

CREATE OR REPLACE FUNCTION prevent_user_deletion()
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

CREATE OR REPLACE TRIGGER prevent_user_deletion_trigger
BEFORE DELETE ON "user"
FOR EACH ROW
EXECUTE FUNCTION prevent_user_deletion();

CREATE TRIGGER automatic_address_deletion_trigger_user
AFTER DELETE ON "user"
FOR EACH ROW
EXECUTE FUNCTION automatic_address_deletion();