USE sp;

CREATE DEFINER=`root`@`localhost` TRIGGER member_afterUpdate
AFTER UPDATE
ON `member` FOR EACH ROW
BEGIN
	IF OLD.isRegistered = 0 AND NEW.isRegistered = 1 THEN
		CALL insertBalance(NEW.id);
	END IF;
	IF OLD.isRegistered = 1 AND NEW.isRegistered = 0 THEN
		DELETE FROM balance
		WHERE memberFk = NEW.id;
	END IF;
END