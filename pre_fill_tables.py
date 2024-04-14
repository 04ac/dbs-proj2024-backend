import csv
import ast
import pandas as pd
from secret_ops import get_connection

# Function to insert authors from CSV into database
def insert_authors_from_csv(csv_file):
    connection = get_connection()
    try:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            with connection:
                with connection.cursor() as cursor:
                    for row in reader:
                        cursor.execute("INSERT INTO Authors (auth_id, name) VALUES (%s, %s)", (row['author_id'], row['author_name']))
    except Exception as e:
        print(f"Error inserting authors: {e}")

# # Path to your CSV file
# csv_file = "authors.csv"  # Replace with the path to your CSV file
#
# # Insert authors from CSV into database
# insert_authors_from_csv(csv_file)


# -------------------------------------------------------------------------------------------------

# Function to insert categories from Excel into database
def insert_categories_from_excel(excel_file):
    connection = get_connection()
    try:
        df = pd.read_excel(excel_file)
        with connection:
            with connection.cursor() as cursor:
                for index, row in df.iterrows():
                    cursor.execute("INSERT INTO Categories (category_id, category) VALUES (%s, %s)", (row['category_id'], row['category']))
    except Exception as e:
        print(f"Error inserting categories: {e}")

# # Path to your Excel file
# excel_file = "categories_final.xlsx"  # Replace with the path to your Excel file
#
# # Insert categories from Excel into database
# insert_categories_from_excel(excel_file)

# -------------------------------------------------------------------------------------------------


# Function to insert editions from Excel into database
def insert_editions_from_excel(excel_file):
    connection = get_connection()
    try:
        df = pd.read_excel(excel_file)
        with connection:
            with connection.cursor() as cursor:
                for index, row in df.iterrows():
                    cursor.execute("INSERT INTO Editions (edition_id, editions) VALUES (%s, %s)", (row['edition_id'], row['edition']))
    except Exception as e:
        print(f"Error inserting editions: {e}")

# # Path to your Excel file
# excel_file = "editions.xlsx"  # Replace with the path to your Excel file
#
# # Insert editions from Excel into database
# insert_editions_from_excel(excel_file)

# ----------------------------------------------------------------------------------------------------


# Function to insert publishers from Excel into database
def insert_publishers_from_excel(excel_file):
    connection = get_connection()
    try:
        df = pd.read_excel(excel_file)
        with connection:
            with connection.cursor() as cursor:
                for index, row in df.iterrows():
                    cursor.execute("INSERT INTO Publisher (publisher_id, name) VALUES (%s, %s)", (row['publisher_id'], row['name']))
    except Exception as e:
        print(f"Error inserting publishers: {e}")

# # Path to your Excel file
# excel_file = "publishers.xlsx"  # Replace with the path to your Excel file
#
# # Insert publishers from Excel into database
# insert_publishers_from_excel(excel_file)

# ----------------------------------------------------------------------------------------------------


# Function to insert formats from Excel into database
def insert_formats_from_excel(excel_file):
    connection = get_connection()
    try:
        df = pd.read_excel(excel_file)
        with connection:
            with connection.cursor() as cursor:
                for index, row in df.iterrows():
                    cursor.execute("INSERT INTO Formats (format_id, format) VALUES (%s, %s)", (row['format_id'], row['format']))
    except Exception as e:
        print(f"Error inserting formats: {e}")

# # Path to your Excel file
# excel_file = "formats.xlsx"  # Replace with the path to your Excel file
#
# # Insert formats from Excel into database
# insert_formats_from_excel(excel_file)

# --------------------------------------------------------------------------------------------------------


# Function to insert data from Excel into Main table
def insert_main_data_from_excel(excel_file):
    connection = get_connection()
    try:
        df = pd.read_excel(excel_file)
        with connection:
            with connection.cursor() as cursor:
                for index, row in df.iterrows():
                    cursor.execute("INSERT INTO Main (book_id, category_id, publisher_id, edition_id, format_id) VALUES (%s, %s, %s, %s, %s)",
                                   (row['book_id'], row['category_id'], row['publisher_id'], row['edition_id'], row['format_id']))
    except Exception as e:
        print(f"Error inserting data into Main table: {e}")

# # Path to your Excel file
# excel_file = "dbms_data_excel.xlsx"  # Replace with the path to your Excel file
#
# # Insert data from Excel into Main table
# insert_main_data_from_excel(excel_file)

# -------------------------------------------------------------------------------------------------------


# Function to insert data from Excel into Physical_Attr table
def insert_physical_attr_from_excel(excel_file):
    connection = get_connection()
    try:
        df = pd.read_excel(excel_file)
        with connection:
            with connection.cursor() as cursor:
                for index, row in df.iterrows():
                    cursor.execute("INSERT INTO Physical_Attr (book_id, x, y, z, w) VALUES (%s, %s, %s, %s, %s)",
                                   (row['book_id'], row['x'], row['y'], row['z'], row['weight']))
    except Exception as e:
        print(f"Error inserting data into Physical_Attr table: {e}")

# Path to your Excel file
# excel_file = "dbms_data_excel.xlsx"  # Replace with the path to your Excel file
#
# # Insert data from Excel into Physical_Attr table
# insert_physical_attr_from_excel(excel_file)


# -----------------------------------------------------------------------------------------------------

# Function to insert data from Excel into Image table
def insert_image_data_from_excel(excel_file):
    connection = get_connection()
    try:
        df = pd.read_excel(excel_file)
        with connection:
            with connection.cursor() as cursor:
                for index, row in df.iterrows():
                    cursor.execute("INSERT INTO Image (book_id, url) VALUES (%s, %s)",
                                   (row['book_id'], row['url']))
    except Exception as e:
        print(f"Error inserting data into Image table: {e}")

# Path to your Excel file
# excel_file = "dbms_data_excel.xlsx"  # Replace with the path to your Excel file
#
# # Insert data from Excel into Image table
# insert_image_data_from_excel(excel_file)

# ------------------------------------------------------------------------------------------------------

# Function to insert data from Excel into ISBN table
def insert_isbn_data_from_excel(excel_file):
    connection = get_connection()
    try:
        df = pd.read_excel(excel_file)
        with connection:
            with connection.cursor() as cursor:
                for index, row in df.iterrows():
                    cursor.execute("INSERT INTO ISBN (book_id, isbn10, isbn13) VALUES (%s, %s, %s)",
                                   (row['book_id'], row['isbn10'], row['isbn13']))
    except Exception as e:
        print(f"Error inserting data into ISBN table: {e}")

# Path to your Excel file
# excel_file = "dbms_data_excel.xlsx"  # Replace with the path to your Excel file
#
# # Insert data from Excel into ISBN table
# insert_isbn_data_from_excel(excel_file)

# -------------------------------------------------------------------------------------------------------

# Function to convert string to date
# def convert_to_date(date_str):
#     try:
#         return datetime.strptime(date_str, "%m-%d-%Y %H:%M:%S").date()
#     except ValueError:
#         return None


# Function to insert data from Excel into Description table
def insert_description_data_from_excel(excel_file):
    connection = get_connection()
    try:
        df = pd.read_excel(excel_file)
        with connection:
            with connection.cursor() as cursor:
                for index, row in df.iterrows():
                    cursor.execute("INSERT INTO Description (book_id, description, title, language, pub_date) VALUES (%s, %s, %s, %s, %s)",
                                   (row['book_id'], row['description'], row['title'], row['language'], row['pub_date']))
    except Exception as e:
        print(f"Error inserting data into Description table: {e}")

# # Path to your Excel file
# excel_file = "dbms_data_excel.xlsx"  # Replace with the path to your Excel file
#
# # Insert data from Excel into Description table
# insert_description_data_from_excel(excel_file)

# ----------------------------------------------------------------------------------------------------------

# Function to insert data from Excel into Ratings table
def insert_ratings_data_from_excel(excel_file):
    connection = get_connection()
    try:
        df = pd.read_excel(excel_file)
        with connection:
            with connection.cursor() as cursor:
                for index, row in df.iterrows():
                    cursor.execute("INSERT INTO Ratings (book_id, rating_avg, rating_count, for_ages) VALUES (%s, %s, %s, %s)",
                                   (row['book_id'], row['rating_avg'], row['rating_count'], row['for_ages']))
    except Exception as e:
        print(f"Error inserting data into Ratings table: {e}")
#
# # Path to your Excel file
# excel_file = "dbms_data_excel.xlsx"  # Replace with the path to your Excel file
#
# # Insert data from Excel into Ratings table
# insert_ratings_data_from_excel(excel_file)

# ---------------------------------------------------------------------------------------------------------

# Function to insert data from Excel into Auth_Book table
def insert_auth_book_data_from_excel(excel_file):
    connection = get_connection()
    try:
        df = pd.read_excel(excel_file)
        with connection:
            with connection.cursor() as cursor:
                for index, row in df.iterrows():
                    author_ids = ast.literal_eval(row['author_ids'])  # Convert string to list
                    for author_id in author_ids:
                        cursor.execute("INSERT INTO Auth_Book (book_id, auth_id) VALUES (%s, %s)",
                                       (row['book_id'], author_id))
    except Exception as e:
        print(f"Error inserting data into Auth_Book table: {e}")

# Path to your Excel file
# excel_file = "dbms_data_excel.xlsx"  # Replace with the path to your Excel file
#
# # Insert data from Excel into Auth_Book table
# insert_auth_book_data_from_excel(excel_file)
