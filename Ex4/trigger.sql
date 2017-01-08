
CREATE OR REPLACE FUNCTION changTime() 
RETURNS TRIGGER AS $time_change$
	BEGIN
    	UPDATE account
        SET last_activity_date = NEW.txn_date
        WHERE account_id = NEW.account_id;
        RETURN NEW;
    END;
$time_change$ LANGUAGE plpgsql;

DROP TRIGGER time_change ON trans;

CREATE TRIGGER time_change
AFTER INSERT ON trans
FOR EACH ROW EXECUTE PROCEDURE changTime();

INSERT INTO trans
VALUES (22,'2016-01-05',3,'DBT',100.00,NULL,NULL,'2008-01-05');

