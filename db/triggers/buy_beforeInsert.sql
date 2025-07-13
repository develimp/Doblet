USE sp;

CREATE DEFINER=`root`@`localhost` TRIGGER buy_beforeInsert
BEFORE INSERT
ON buy FOR EACH ROW
BEGIN
	CALL getCurrentFallaYear(NEW.fallaYearFk);
END