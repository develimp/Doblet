DROP PROCEDURE IF EXISTS sp.regenerateBalance;

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp`.`regenerateBalance`()
/*
* Elimina el contingut de la taula balance i la regenera amb les dades actuals.
*/

BEGIN
    DECLARE vDone INT DEFAULT 0;
    DECLARE vId INT;
    DECLARE vCursor CURSOR FOR 
        SELECT id
            FROM member
            WHERE isRegistered = 1;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET vDone = 1;

    DELETE FROM balance;

    OPEN vCursor;

    read_loop: LOOP
        FETCH vCursor INTO vId;
        IF vDone THEN
            LEAVE read_loop;
        END IF;

        CALL sp.insertBalance(vId);
    END LOOP read_loop;

    CLOSE vCursor;
END