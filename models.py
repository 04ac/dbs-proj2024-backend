from pydantic import BaseModel


class Room(BaseModel):
    name: str


class Temperature(BaseModel):
    temperature: float
    room_id: int
    date: str = None


# Model for Author
class Author(BaseModel):
    name: str

# Model for Category
class Category(BaseModel):
    category: str

# Model for Publisher
class Publisher(BaseModel):
    name: str

# Model for Edition
class Edition(BaseModel):
    editions: str

# Model for Format
class Format(BaseModel):
    format: str

# Model for Customer
class Customer(BaseModel):
    name: str
    last_visit: str

# Model for Main
class Main(BaseModel):
    category_id: int
    publisher_id: int
    edition_id: int
    format_id: int

# Model for Physical_Attr
class PhysicalAttr(BaseModel):
    x: int
    y: int
    z: int
    w: int

# Model for Image
class Image(BaseModel):
    url: str

# Model for ISBN
class ISBN(BaseModel):
    isbn10: str
    isbn13: str

# Model for Description
class Description(BaseModel):
    description: str
    language: str
    pub_date: str

# Model for Ratings
class Rating(BaseModel):
    rating_avg: float
    rating_count: int
    for_ages: str

# Model for BookIssued
class BookIssued(BaseModel):
    customer_id: int
    book_id: int

# Model for Recommendation
class Recommendation(BaseModel):
    customer_id: int
    book_id: int

# Model for AuthBook
class AuthBook(BaseModel):
    book_id: int
    auth_id: int
