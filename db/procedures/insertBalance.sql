DROP PROCEDURE IF EXISTS sp.insertBalance;

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp`.`insertBalance`(
	IN vId INT
)
/*
* A partir de l'id del faller inserta les seues dades d'assignacions
* i pagaments a la taula balance.
*
* @params vId: int
*/
BEGIN
	DECLARE vFallaYearFk INT;
	DECLARE vInitialFeeAssigned DECIMAL(10, 2);
	DECLARE vFamilyDiscount DECIMAL(10, 2);
	DECLARE vTotalFeeAssigned DECIMAL(10,2) DEFAULT 0;
	DECLARE vTotalFeePayed DECIMAL(10,2) DEFAULT 0;
	DECLARE vTotalLotteryAssigned DECIMAL(10,2) DEFAULT 0;
	DECLARE vTotalLotteryPayed DECIMAL(10,2) DEFAULT 0;
	DECLARE vTotalRaffleAssigned DECIMAL(10,2) DEFAULT 0;
	DECLARE vTotalRafflePayed DECIMAL(10,2) DEFAULT 0;
	
	CALL getCurrentFallaYear(vFallaYearFk);
	
	SELECT fee INTO vInitialFeeAssigned
		FROM category c
			JOIN member m ON c.id = m.categoryFk
		WHERE m.id = vId;
	
	SELECT discount INTO vFamilyDiscount
		FROM family f
			JOIN member m ON f.id = m.familyFk
		WHERE m.id = vId;

	SELECT IFNULL(SUM(amount), 0) INTO vTotalFeeAssigned
		FROM movement
		WHERE memberFk = vId
			AND fallaYearFk = vFallaYearFk
			AND idType = 1
			AND idConcept = 1;
	
	SET vInitialFeeAssigned = vInitialFeeAssigned - (vFamilyDiscount * vInitialFeeAssigned / 100);
	SET vTotalFeeAssigned = vTotalFeeAssigned + vInitialFeeAssigned;

	SELECT IFNULL(SUM(amount), 0) INTO vTotalFeePayed
		FROM movement
		WHERE memberFk = vId
			AND fallaYearFk = vFallaYearFk
			AND idType = 2
			AND idConcept = 1;

	SELECT IFNULL(SUM(amount), 0) INTO vTotalLotteryAssigned
		FROM movement
		WHERE memberFk = vId
			AND fallaYearFk = vFallaYearFk
			AND idType = 1
			AND idConcept = 2;

	SELECT IFNULL(SUM(amount), 0) INTO vTotalLotteryPayed
		FROM movement
		WHERE memberFk = vId
			AND fallaYearFk = vFallaYearFk
			AND idType = 2
			AND idConcept = 2;

	SELECT IFNULL(SUM(amount), 0) INTO vTotalRaffleAssigned
		FROM movement
		WHERE memberFk = vId
			AND fallaYearFk = vFallaYearFk
			AND idType = 1
			AND idConcept = 3;

	SELECT IFNULL(SUM(amount), 0) INTO vTotalRafflePayed
		FROM movement
		WHERE memberFk = vId
			AND fallaYearFk = vFallaYearFk
			AND idType = 2
			AND idConcept = 3;

	INSERT INTO balance (memberFk, feeAssigned, feePayed, lotteryAssigned, lotteryPayed, raffleAssigned, rafflePayed)
		VALUES (vId, vTotalFeeAssigned, vTotalFeePayed, vTotalLotteryAssigned, vTotalLotteryPayed, vTotalRaffleAssigned, vTotalRafflePayed);		
END