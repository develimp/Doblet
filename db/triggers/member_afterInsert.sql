USE sp;

CREATE DEFINER=`root`@`localhost` TRIGGER member_afterInsert
AFTER INSERT
ON `member` FOR EACH ROW
BEGIN
	CALL insertBalance(NEW.id);

	IF NEW.isRegistered = 1 THEN
    	INSERT INTO memberStatusLog(memberFk, status)
    		VALUES (NEW.id, 1);
  	END IF;
END