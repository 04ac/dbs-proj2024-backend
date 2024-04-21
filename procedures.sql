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
