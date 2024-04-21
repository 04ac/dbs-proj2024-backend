from datetime import datetime

from fastapi import FastAPI, HTTPException
from models import *
from connect_db import get_connection
from recommend import recommender

app = FastAPI()


# Function to establish database connection
def get_db_connection():
    return get_connection()


# Endpoint to execute the SQL query and return the result
@app.get("/books/")
def get_books():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("""
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
                """)
                result = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        connection.close()

    # Convert the result to list of dictionaries
    books = []
    for row in result:
        book = {
            "book_id": row[0],
            "title": row[1],
            "Description": row[2],
            "date_published": row[3].isoformat() if row[3] else None,
            "rating": row[4],
            "rating_count": row[5],
            "categories": row[6],
            "for_ages": row[7],
            "authors": row[8],
            "image_url": row[9],
            "format": row[10],
            "publisher": row[11],
            "isbn": row[12],
            "edition": row[13],
            "dimension_x": row[14],
            "dimension_y": row[15],
            "dimension_z": row[16],
            "dimension_w": row[17]
        }
        books.append(book)

    return {"books": books}



@app.get("/recommend/{index}")
def get_recommendation(index: int):
    return {"recommendations": recommender(index)}


# Create Author
@app.post("/authors/")
def create_author(author: Author):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Authors (name) VALUES (%s) RETURNING auth_id", (author.name,))
                auth_id = cursor.fetchone()[0]
        return {"auth_id": auth_id, "name": author.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all Authors
@app.get("/authors/")
def get_all_authors():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Authors")
                authors = cursor.fetchall()
        return {"authors": authors}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create Category
@app.post("/categories/")
def create_category(category: Category):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Categories (category) VALUES (%s) RETURNING category_id",
                               (category.category,))
                category_id = cursor.fetchone()[0]
        return {"category_id": category_id, "category": category.category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all Categories
@app.get("/categories/")
def get_all_categories():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Categories")
                categories = cursor.fetchall()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create Publisher
@app.post("/publishers/")
def create_publisher(publisher: Publisher):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Publisher (name) VALUES (%s) RETURNING publisher_id", (publisher.name,))
                publisher_id = cursor.fetchone()[0]
        return {"publisher_id": publisher_id, "name": publisher.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all Publishers
@app.get("/publishers/")
def get_all_publishers():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Publisher")
                publishers = cursor.fetchall()
        return {"publishers": publishers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create Edition
@app.post("/editions/")
def create_edition(edition: Edition):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Editions (editions) VALUES (%s) RETURNING edition_id", (edition.editions,))
                edition_id = cursor.fetchone()[0]
        return {"edition_id": edition_id, "editions": edition.editions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all Editions
@app.get("/editions/")
def get_all_editions():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Editions")
                editions = cursor.fetchall()
        return {"editions": editions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create Format
@app.post("/formats/")
def create_format(format: Format):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Formats (format) VALUES (%s) RETURNING format_id", (format.format,))
                format_id = cursor.fetchone()[0]
        return {"format_id": format_id, "format": format.format}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all Formats
@app.get("/formats/")
def get_all_formats():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Formats")
                formats = cursor.fetchall()
        return {"formats": formats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/customers/")
def create_customer(customer: Customer):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Customers (name, account_created, passwd) VALUES (%s, %s, %s) RETURNING customer_id",
                    (customer.name, customer.account_created, customer.passwd)
                )
                customer_id = cursor.fetchone()[0]
        return {
            "customer_id": customer_id,
            "name": customer.name,
            "account_created": customer.account_created.isoformat(),  # Convert date to ISO format for response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all Customers
@app.get("/customers/")
def get_all_customers():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Customers")
                customers = cursor.fetchall()
        return {"customers": customers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# For customer auth
@app.get("/customer-auth/{name}/{passwd}")
def get_all_customers(name: str, passwd: str):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Customers where name='" + name + "' and passwd='" + passwd + "';")
                customers = cursor.fetchall()
        return {"customer": customers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create Main
@app.post("/main/")
def create_main(main: Main):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Main (category_id, publisher_id, edition_id, format_id) VALUES (%s, %s, %s, %s) RETURNING book_id",
                    (main.category_id, main.publisher_id, main.edition_id, main.format_id,))
                book_id = cursor.fetchone()[0]
        return {"book_id": book_id, "category_id": main.category_id, "publisher_id": main.publisher_id,
                "edition_id": main.edition_id, "format_id": main.format_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all Main records
@app.get("/main/")
def get_all_main():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Main")
                main_records = cursor.fetchall()
        return {"main_records": main_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create Physical_Attr
@app.post("/physical-attr/")
def create_physical_attr(physical_attr: PhysicalAttr):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Physical_Attr (x, y, z, w) VALUES (%s, %s, %s, %s) RETURNING book_id",
                               (physical_attr.x, physical_attr.y, physical_attr.z, physical_attr.w,))
                book_id = cursor.fetchone()[0]
        return {"book_id": book_id, "x": physical_attr.x, "y": physical_attr.y, "z": physical_attr.z,
                "w": physical_attr.w}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all Physical_Attr records
@app.get("/physical-attr/")
def get_all_physical_attr():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Physical_Attr")
                physical_attr_records = cursor.fetchall()
        return {"physical_attr_records": physical_attr_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create Image
@app.post("/images/")
def create_image(image: Image):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Image (url) VALUES (%s) RETURNING book_id", (image.url,))
                book_id = cursor.fetchone()[0]
        return {"book_id": book_id, "url": image.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all Image records
@app.get("/images/")
def get_all_images():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Image")
                image_records = cursor.fetchall()
        return {"image_records": image_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create ISBN
@app.post("/isbn/")
def create_isbn(isbn: ISBN):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO ISBN (isbn10, isbn13) VALUES (%s, %s) RETURNING book_id",
                               (isbn.isbn10, isbn.isbn13,))
                book_id = cursor.fetchone()[0]
        return {"book_id": book_id, "isbn10": isbn.isbn10, "isbn13": isbn.isbn13}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all ISBN records
@app.get("/isbn/")
def get_all_isbn():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM ISBN")
                isbn_records = cursor.fetchall()
        return {"isbn_records": isbn_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create Description
@app.post("/descriptions/")
def create_description(description: Description):
    connection = get_db_connection()
    try:
        # Convert string pub_date to date object
        pub_date = datetime.strptime(description.pub_date, "%Y-%m-%d").date()

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Description (description, language, pub_date) VALUES (%s, %s, %s) RETURNING book_id",
                    (description.description, description.language, pub_date,))
                book_id = cursor.fetchone()[0]
        return {"book_id": book_id, "description": description.description, "language": description.language,
                "pub_date": pub_date}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all Description records
@app.get("/descriptions/")
def get_all_descriptions():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Description")
                description_records = cursor.fetchall()
        return {"description_records": description_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create Ratings
@app.post("/ratings/")
def create_rating(rating: Rating):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Ratings (rating_avg, rating_count, for_ages) VALUES (%s, %s, %s) RETURNING rating_id",
                    (rating.rating_avg, rating.rating_count, rating.for_ages,))
                rating_id = cursor.fetchone()[0]
        return {"rating_id": rating_id, "rating_avg": rating.rating_avg, "rating_count": rating.rating_count,
                "for_ages": rating.for_ages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all Ratings records
@app.get("/ratings/")
def get_all_ratings():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Ratings")
                rating_records = cursor.fetchall()
        return {"rating_records": rating_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# returns a list of recommendations after adding to wishlist
@app.post("/wishlist/")
def add_to_wishlist(book_issued: BookIssued):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("CALL wishlist_package.insert_wishlist(%s, %s)",
                               (int(book_issued.customer_id), int(book_issued.book_id)))

                recommendations = recommender(book_issued.book_id)

                cursor.execute("DELETE FROM recommendations WHERE customer_id = %s", (book_issued.customer_id,))

                for recommendation in recommendations:
                    cursor.execute("CALL wishlist_package.insert_recommendations(%s, %s)",
                                   (int(book_issued.customer_id), int(recommendation) + 1))

        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()


# Get all Wishlist records
@app.get("/wishlist/{customer_id}")
def get_wishlist(customer_id: int):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM wishlist where customer_id=" + str(customer_id) + ";")
                wishlist = cursor.fetchall()
        return {"wishlist": wishlist}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/wishlist/{customer_id}/{book_id}")
def delete_wishlist_item(customer_id: int, book_id: int):
    try:
        connection = get_db_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DO $$
                    BEGIN
                        DELETE FROM WISHLIST WHERE customer_id = %s AND book_id = %s;
                        IF NOT FOUND THEN
                            RAISE EXCEPTION 'Record with customer_id %s and book_id %s not found';
                        END IF;
                    END $$;
                    """, (customer_id, book_id, customer_id, book_id)
                )
        return {"message": f"Record with customer_id {customer_id} and book_id {book_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create Recommendation
@app.post("/recommendations/")
def create_recommendation(recommendation: Recommendation):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Recommendations (customer_id, book_id) VALUES (%s, %s)",
                               (recommendation.customer_id, recommendation.book_id,))
        return {"customer_id": recommendation.customer_id, "book_id": recommendation.book_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all Recommendation records
@app.get("/recommendations/")
def get_all_recommendations():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Recommendations")
                recommendation_records = cursor.fetchall()
        return {"recommendation_records": recommendation_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create AuthBook
@app.post("/auth-books/")
def create_auth_book(auth_book: AuthBook):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Auth_Book (book_id, auth_id) VALUES (%s, %s)",
                               (auth_book.book_id, auth_book.auth_id,))
        return {"book_id": auth_book.book_id, "auth_id": auth_book.auth_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all AuthBook records
@app.get("/auth-books/")
def get_all_auth_books():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Auth_Book")
                auth_book_records = cursor.fetchall()
        return {"auth_book_records": auth_book_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
