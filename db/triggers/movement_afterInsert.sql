USE sp;

CREATE DEFINER=`root`@`localhost` TRIGGER movement_afterInsert
AFTER INSERT
ON movement FOR EACH ROW
BEGIN
	UPDATE balance
	SET
		feeAssigned = feeAssigned + IF(NEW.idType = 1 AND NEW.idConcept = 1, NEW.amount, 0),
		feePayed = feePayed + IF(NEW.idType = 2 AND NEW.idConcept = 1, NEW.amount, 0),
		lotteryAssigned = lotteryAssigned + IF(NEW.idType = 1 AND NEW.idConcept = 2, NEW.amount, 0),
		lotteryPayed = lotteryPayed + IF(NEW.idType = 2 AND NEW.idConcept = 2, NEW.amount, 0),
		raffleAssigned = raffleAssigned + IF(NEW.idType = 1 AND NEW.idConcept = 3, NEW.amount, 0),
		rafflePayed = rafflePayed + IF(NEW.idType = 2 AND NEW.idConcept = 3, NEW.amount, 0)
	WHERE
		memberFk = NEW.memberFk;
END
