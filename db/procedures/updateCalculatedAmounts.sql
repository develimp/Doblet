DROP PROCEDURE IF EXISTS sp.updateCalculatedAmounts;

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp`.`updateCalculatedAmounts`(IN vMonthsRemaining INT)
BEGIN
    UPDATE directDebit dd
    JOIN (
        SELECT
            m.directDebitFk,
            SUM(b.feeAssigned + b.raffleAssigned - b.feePayed - b.rafflePayed) totalDebt
        FROM member m
        	JOIN balance b ON b.memberFk = m.id
        WHERE m.directDebitFk IS NOT NULL
        GROUP BY m.directDebitFk
    ) sub ON sub.directDebitFk = dd.id
    SET dd.calculatedAmount = ROUND(sub.totalDebt / vMonthsRemaining, 2);
END