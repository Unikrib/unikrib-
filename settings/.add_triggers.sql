-- This adds a trigger to the review table to update the ratings on the users table

DELIMITER // ;
DROP TRIGGER IF EXISTS calc_avg;
CREATE TRIGGER calc_avg
    AFTER INSERT ON reviews
    FOR EACH ROW
    BEGIN
        UPDATE users
        SET rating = (
            SELECT AVG(star)
            FROM reviews
            WHERE reviewee = NEW.reviewee
        )
        WHERE id = NEW.reviewee;
    END//
DELIMITER ;
