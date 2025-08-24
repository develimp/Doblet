USE sp;

CREATE DEFINER=CURRENT_USER TRIGGER directDebit_afterDelete
AFTER DELETE 
ON directDebit FOR EACH ROW
BEGIN
  UPDATE member
  SET directDebitFk = NULL
  WHERE id = OLD.memberFk;
END