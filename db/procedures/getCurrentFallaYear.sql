DROP PROCEDURE IF EXISTS sp.getCurrentFallaYear;

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp`.`getCurrentFallaYear`(INOUT vFallaYear INT)
BEGIN
	DECLARE vLastFallaYear INT;

	SELECT code INTO vLastFallaYear
	FROM fallaYear ORDER BY code DESC LIMIT 1;

	IF vFallaYear IS NULL THEN
		SET vFallaYear = vLastFallaYear;
	END IF;
END