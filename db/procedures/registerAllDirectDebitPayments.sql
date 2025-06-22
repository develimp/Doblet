DROP PROCEDURE IF EXISTS sp.calculateFallaYear;

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp`.`registerAllDirectDebitPayments`(
	IN in_transaction_date DATE,
    IN in_description TEXT
)
BEGIN
    DECLARE done_dd INT DEFAULT FALSE;
    DECLARE v_dd_id INT;
    DECLARE v_dd_amount DECIMAL(10,2);
    DECLARE v_fallaYearFk INT;

    DECLARE cur_dd CURSOR FOR
        SELECT id, actualAmount FROM directDebit;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done_dd = TRUE;
    
    SELECT code INTO v_fallaYearFk
    	FROM fallaYear
    	ORDER BY code DESC
    	LIMIT 1;

    OPEN cur_dd;

    dd_loop: LOOP
        FETCH cur_dd INTO v_dd_id, v_dd_amount;
        IF done_dd THEN
            LEAVE dd_loop;
        END IF;

        BEGIN
            DECLARE done_mb INT DEFAULT FALSE;
            DECLARE v_member_id INT;
            DECLARE v_pending DECIMAL(10,2);
            DECLARE v_payment DECIMAL(10,2);

            DECLARE cur_mb CURSOR FOR
                SELECT id FROM member WHERE directDebitFk = v_dd_id ORDER BY id;

            DECLARE CONTINUE HANDLER FOR NOT FOUND SET done_mb = TRUE;

            OPEN cur_mb;

            fee_loop: LOOP
                FETCH cur_mb INTO v_member_id;
                IF done_mb THEN
                    LEAVE fee_loop;
                END IF;

                IF v_dd_amount <= 0 THEN
                    LEAVE fee_loop;
                END IF;

                SELECT (feeAssigned - feePayed)
                	INTO v_pending
                	FROM balance
                	WHERE memberFk = v_member_id;

                IF v_pending > 0 THEN
                    SET v_payment = LEAST(v_pending, v_dd_amount);

                    INSERT INTO movement (
                        transactionDate, amount, idType, idConcept,
                        memberFk, fallaYearFk, description
                    ) VALUES (
                        in_transaction_date, v_payment, 2, 1,
                        v_member_id, v_fallaYearFk, in_description
                    );

                    SET v_dd_amount = v_dd_amount - v_payment;
                END IF;
            END LOOP;

            CLOSE cur_mb;
        END;

        BEGIN
            DECLARE done_mb INT DEFAULT FALSE;
            DECLARE v_member_id INT;
            DECLARE v_pending DECIMAL(10,2);
            DECLARE v_payment DECIMAL(10,2);

            DECLARE cur_mb CURSOR FOR
                SELECT id FROM member WHERE directDebitFk = v_dd_id ORDER BY id;

            DECLARE CONTINUE HANDLER FOR NOT FOUND SET done_mb = TRUE;

            OPEN cur_mb;

            raffle_loop: LOOP
                FETCH cur_mb INTO v_member_id;
                IF done_mb THEN
                    LEAVE raffle_loop;
                END IF;

                IF v_dd_amount <= 0 THEN
                    LEAVE raffle_loop;
                END IF;

                SELECT (raffleAssigned - rafflePayed)
                	INTO v_pending
                	FROM balance
                	WHERE memberFk = v_member_id;

                IF v_pending > 0 THEN
                    SET v_payment = LEAST(v_pending, v_dd_amount);

                    INSERT INTO movement (
                        transactionDate, amount, idType, idConcept,
                        memberFk, fallaYearFk, description
                    ) VALUES (
                        in_transaction_date, v_payment, 2, 3,
                        v_member_id, v_fallaYearFk, in_description
                    );

                    SET v_dd_amount = v_dd_amount - v_payment;
                END IF;
            END LOOP;

            CLOSE cur_mb;
        END;

    END LOOP;

    CLOSE cur_dd;
END