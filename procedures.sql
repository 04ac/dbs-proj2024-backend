-- Package in PostgreSQL
CREATE SCHEMA wishlist_package;

CREATE OR REPLACE PROCEDURE wishlist_package.insert_wishlist(customer_id INT, book_id INT) AS $$
BEGIN
  INSERT INTO wishlist (customer_id, book_id) VALUES (customer_id, book_id);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE wishlist_package.insert_recommendations(customer_id INT, book_id INT) AS $$
BEGIN
  INSERT INTO recommendations (customer_id, book_id) VALUES (customer_id, book_id);
END;
$$ LANGUAGE plpgsql;


-- Trigger to fill up date account created
CREATE OR REPLACE FUNCTION insert_account_created()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO Customer_Account_Created (customer_id, account_created)
    VALUES (NEW.customer_id, CURRENT_DATE);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER account_created_trigger
AFTER INSERT ON Customers
FOR EACH ROW
EXECUTE FUNCTION insert_account_created();

