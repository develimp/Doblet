USE sp;

CREATE DEFINER=`root`@`localhost` TRIGGER member_afterInsert
AFTER INSERT
ON `member` FOR EACH ROW
BEGIN
	CALL insertBalance(NEW.id);
END