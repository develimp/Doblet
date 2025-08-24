USE sp;

CREATE DEFINER=CURRENT_USER TRIGGER directDebit_beforeInsert
BEFORE INSERT 
ON directDebit FOR EACH ROW
BEGIN
  DECLARE existingFk INT;

  SELECT directDebitFk
  	INTO existingFk
  	FROM member
 	 WHERE id = NEW.memberFk;

  IF existingFk IS NOT NULL THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Aquest membre ja té una domiciliació assignada';
  END IF;
END