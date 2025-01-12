DROP PROCEDURE IF EXISTS sp.upsertMembershipHistory;

CREATE DEFINER=`root`@`localhost` PROCEDURE sp.upsertMembershipHistory(
	IN vMemberFk INT, 
    IN vFallaYearFk INT, 
    IN vFalla VARCHAR(50), 
    IN vPosition VARCHAR(30)
)
BEGIN
	DECLARE vCreated DATE;
    DECLARE vFinished DATE;

    SET vCreated = CONCAT(vFallaYearFk - 1, '-03-20');
    SET vFinished = CONCAT(vFallaYearFk, '-03-19');

    IF NOT EXISTS (
        SELECT 1 FROM fallaYear WHERE code = vFallaYearFk
    ) THEN
        INSERT INTO fallaYear (code, created, finished)
        VALUES (vFallaYearFk, vCreated, vFinished);
    END IF;

    IF EXISTS (
        SELECT 1 FROM membershipHistory
        WHERE memberFk = vMemberFk AND fallaYearFk = vFallaYearFk
    ) THEN
        UPDATE membershipHistory
        SET falla = vFalla, `position` = vPosition
        WHERE memberFk = vMemberFk AND fallaYearFk = vFallaYearFk;
    ELSE
        INSERT INTO membershipHistory (memberFk, fallaYearFk, falla, `position`)
        VALUES (vMemberFk, vFallaYearFk, vFalla, vPosition);
    END IF;
END