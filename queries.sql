SELECT
    m.book_id,
    d.title,
    d.Description,
    d.pub_date AS date_published,
    r.rating_avg AS rating,
    r.rating_count AS rating_count,
    c.category AS categories,
    r.for_ages AS for_ages,
    json_agg(a.name) AS authors,
    i.url AS image_url,
    f.format AS format,
    p.name AS publisher,
    isbn.isbn10 AS isbn,
    e.editions AS edition,
    pa.x AS dimension_x,
    pa.y AS dimension_y,
    pa.z AS dimension_z,
    pa.w AS dimension_w
FROM
    Main m
JOIN
    Description d ON m.book_id = d.book_id
JOIN
    Ratings r ON m.book_id = r.book_id
JOIN
    Auth_Book ab ON m.book_id = ab.book_id
JOIN
    Authors a ON ab.auth_id = a.auth_id
JOIN
    Categories c ON m.category_id = c.category_id
LEFT JOIN
    Image i ON m.book_id = i.book_id
LEFT JOIN
    Formats f ON m.format_id = f.format_id
LEFT JOIN
    Publisher p ON m.publisher_id = p.publisher_id
LEFT JOIN
    ISBN isbn ON m.book_id = isbn.book_id
LEFT JOIN
    Editions e ON m.edition_id = e.edition_id
LEFT JOIN
    Physical_Attr pa ON m.book_id = pa.book_id
GROUP BY
    m.book_id,
    d.title,
    d.Description,
    d.pub_date,
    r.rating_avg,
    c.category,
    r.rating_count,
    r.for_ages,
    i.url,
    f.format,
    p.name,
    isbn.isbn10,
    e.editions,
    pa.x,
    pa.y,
    pa.z,
    pa.w;


---------------------------------------------------------------------------

"SELECT book_id FROM recommendations where customer_id=" + str(customer_id) + ";"

------------------------------------------------------------------------------------

"INSERT INTO Authors (name) VALUES (%s) RETURNING auth_id", (author.name,)

----------------------------------------------------------------------------------

"SELECT * FROM Authors"

-------------------------------------------------------------------------

"INSERT INTO Categories (category) VALUES (%s) RETURNING category_id",
                               (category.category,)

--------------------------------------------------------------------------------------------

"SELECT * FROM Categories"

------------------------------------------------------------------------------------------

"INSERT INTO Publisher (name) VALUES (%s) RETURNING publisher_id", (publisher.name,)

-----------------------------------------------------------------

"SELECT * FROM Publisher"

---------------------------------------------------------------

"INSERT INTO Editions (editions) VALUES (%s) RETURNING edition_id", (edition.editions,)

----------------------------------------------------------------------

"SELECT * FROM Editions"

-----------------------------------------------------------------------

"INSERT INTO Formats (format) VALUES (%s) RETURNING format_id", (format.format,)

---------------------------------------------------------------------

"SELECT * FROM Formats"

-----------------------------------------

"INSERT INTO Customers (name, passwd) VALUES (%s, %s) RETURNING customer_id",
                    (customer.name, customer.passwd)

---------------------------------------------------------------------

"SELECT * FROM Customers"

------------------------------------------------------------------------

"SELECT * FROM Customers where name='" + name + "' and passwd='" + passwd + "';"

--------------------------------------------------------------------------

"INSERT INTO Main (category_id, publisher_id, edition_id, format_id) VALUES (%s, %s, %s, %s) RETURNING book_id",
                    (main.category_id, main.publisher_id, main.edition_id, main.format_id,)

-------------------------------------------------------------------

"SELECT * FROM Main"

--------------------------------------------------------

"INSERT INTO Physical_Attr (x, y, z, w) VALUES (%s, %s, %s, %s) RETURNING book_id",
                               (physical_attr.x, physical_attr.y, physical_attr.z, physical_attr.w,)

------------------------------------------------------------------------

"SELECT * FROM Physical_Attr"

----------------------------------------------------------------

"INSERT INTO Image (url) VALUES (%s) RETURNING book_id", (image.url,)

----------------------------------------------------------------------------------

"SELECT * FROM Image"

-----------------------------------------------------------------

"INSERT INTO ISBN (isbn10, isbn13) VALUES (%s, %s) RETURNING book_id",
                               (isbn.isbn10, isbn.isbn13,)

---------------------------------------------------------

"SELECT * FROM ISBN"

-------------------------------------------------

"INSERT INTO Description (description, language, pub_date) VALUES (%s, %s, %s) RETURNING book_id",
                    (description.description, description.language, pub_date,)

-----------------------------------------------------

"SELECT * FROM Description"

----------------------------------------------------------

"INSERT INTO Ratings (rating_avg, rating_count, for_ages) VALUES (%s, %s, %s) RETURNING rating_id",
                    (rating.rating_avg, rating.rating_count, rating.for_ages,)

-----------------------------------------------------------

"SELECT * FROM Ratings"

------------------------------------------------

"CALL wishlist_package.insert_wishlist(%s, %s)",
                               (int(book_issued.customer_id), int(book_issued.book_id))

-----------------------------------------------------------------

"DELETE FROM recommendations WHERE customer_id = %s", (book_issued.customer_id,)

--------------------------------------------------------

"CALL wishlist_package.insert_recommendations(%s, %s)",
                                   (int(book_issued.customer_id), int(recommendation) + 1)

----------------------------------------------------

"SELECT * FROM wishlist where customer_id=" + str(customer_id) + ";"

----------------------------------------------------

"""
DO $$
BEGIN
    DELETE FROM WISHLIST WHERE customer_id = %s AND book_id = %s;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Record with customer_id %s and book_id %s not found';
    END IF;
END $$;
""", (customer_id, book_id, customer_id, book_id)

---------------------------------------------------------

"INSERT INTO Recommendations (customer_id, book_id) VALUES (%s, %s)",
                               (recommendation.customer_id, recommendation.book_id,)

------------------------------------------------------

"SELECT * FROM Recommendations"

-----------------------------------------------

"INSERT INTO Auth_Book (book_id, auth_id) VALUES (%s, %s)",
                               (auth_book.book_id, auth_book.auth_id,)

----------------------------------------------------

"SELECT * FROM Auth_Book"