from datetime import datetime

from fastapi import FastAPI, HTTPException
from models import *
from connect_db import get_connection

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
                        i.url AS image_url
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
                    GROUP BY 
                        m.book_id,
                        d.title,
                        d.Description,
                        d.pub_date,
                        r.rating_avg,
                        c.category,
                        r.rating_count,
                        r.for_ages,
                        i.url;
                """)
                result = cursor.fetchall()
    except Exception as e:
        return {"error": str(e)}
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
            "image_url": row[9]
        }
        books.append(book)

    return {"books": books}


# Create Author
@app.post("/authors/")
async def create_author(author: Author):
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
async def get_all_authors():
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
async def create_category(category: Category):
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
async def get_all_categories():
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
async def create_publisher(publisher: Publisher):
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
async def get_all_publishers():
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
async def create_edition(edition: Edition):
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
async def get_all_editions():
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
async def create_format(format: Format):
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
async def get_all_formats():
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


# Create Main
@app.post("/main/")
async def create_main(main: Main):
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
async def get_all_main():
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
async def create_physical_attr(physical_attr: PhysicalAttr):
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
async def get_all_physical_attr():
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
async def create_image(image: Image):
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
async def get_all_images():
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
async def create_isbn(isbn: ISBN):
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
async def get_all_isbn():
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
async def create_description(description: Description):
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
async def get_all_descriptions():
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
async def create_rating(rating: Rating):
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
async def get_all_ratings():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Ratings")
                rating_records = cursor.fetchall()
        return {"rating_records": rating_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create BookIssued
@app.post("/wishlist/")
async def add_to_wishlist(book_issued: BookIssued):
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO wishlist (customer_id, book_id) VALUES (%s, %s)",
                               (book_issued.customer_id, book_issued.book_id,))
        return {"customer_id": book_issued.customer_id, "book_id": book_issued.book_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all BookIssued records
@app.get("/wishlist/")
async def get_wishlist():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM wishlist")
                wishlist = cursor.fetchall()
        return {"wishlist": wishlist}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Create Recommendation
@app.post("/recommendations/")
async def create_recommendation(recommendation: Recommendation):
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
async def get_all_recommendations():
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
async def create_auth_book(auth_book: AuthBook):
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
async def get_all_auth_books():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Auth_Book")
                auth_book_records = cursor.fetchall()
        return {"auth_book_records": auth_book_records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
