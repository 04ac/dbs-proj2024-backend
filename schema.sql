CREATE TABLE IF NOT EXISTS Authors (
    auth_id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Categories (
    category_id SERIAL PRIMARY KEY,
    category VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Publisher (
    publisher_id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Editions (
    edition_id SERIAL PRIMARY KEY,
    editions VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Formats (
    format_id SERIAL PRIMARY KEY,
    format VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    passwd VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Main (
    book_id SERIAL PRIMARY KEY,
    category_id INT,
    publisher_id INT,
    edition_id INT,
    format_id INT,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE CASCADE,
    FOREIGN KEY (publisher_id) REFERENCES Publisher(publisher_id) ON DELETE CASCADE,
    FOREIGN KEY (edition_id) REFERENCES Editions(edition_id) ON DELETE CASCADE,
    FOREIGN KEY (format_id) REFERENCES Format(format_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Physical_Attr (
    book_id SERIAL PRIMARY KEY,
    x INT,
    y INT,
    z INT,
    w INT,
    FOREIGN KEY (book_id) REFERENCES Main(book_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Image (
    book_id SERIAL PRIMARY KEY,
    url VARCHAR(255),
    FOREIGN KEY (book_id) REFERENCES Main(book_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ISBN (
    book_id SERIAL PRIMARY KEY,
    isbn10 VARCHAR(20),
    isbn13 VARCHAR(20),
    FOREIGN KEY (book_id) REFERENCES Main(book_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Description (
    book_id SERIAL PRIMARY KEY,
    description TEXT,
    title TEXT,
    language VARCHAR(50),
    pub_date DATE,
    FOREIGN KEY (book_id) REFERENCES Main(book_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Ratings (
    rating_id SERIAL PRIMARY KEY,
    book_id INT,
    rating_avg FLOAT,
    rating_count INT,
    for_ages VARCHAR(50),
    FOREIGN KEY (book_id) REFERENCES Main(book_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS WISHLIST (
    customer_id INT,
    book_id INT,
    PRIMARY KEY (customer_id, book_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Main(book_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Recommendations (
    recommendation_id SERIAL PRIMARY KEY,
    customer_id INT,
    book_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Main(book_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Auth_Book (
    book_id INT,
    auth_id INT,
    PRIMARY KEY (book_id, auth_id),
    FOREIGN KEY (book_id) REFERENCES Main(book_id) ON DELETE CASCADE,
    FOREIGN KEY (auth_id) REFERENCES Authors(auth_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS CustomerLogin (
    customer_id INT,
    last_login TIMESTAMP,
    PRIMARY KEY (customer_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
);
