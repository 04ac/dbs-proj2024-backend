CREATE_ROOMS_TABLE = (
    "CREATE TABLE IF NOT EXISTS rooms (id SERIAL PRIMARY KEY, name TEXT);"
)
CREATE_TEMPS_TABLE = """CREATE TABLE IF NOT EXISTS temperatures (room_id INTEGER, temperature REAL, 
                        date TIMESTAMP, FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE);"""

INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"
INSERT_TEMP = (
    "INSERT INTO temperatures (room_id, temperature, date) VALUES (%s, %s, %s);"
)
GET_ALL_TEMPERATURES = (
    """SELECT * FROM temperatures"""
)
GLOBAL_NUMBER_OF_DAYS = (
    """SELECT COUNT(DISTINCT DATE(date)) AS days FROM temperatures;"""
)
GLOBAL_AVG = """SELECT AVG(temperature) as average FROM temperatures;"""
ROOM_NAME = """SELECT name FROM rooms WHERE id = (%s)"""
ROOM_NUMBER_OF_DAYS = """SELECT COUNT(DISTINCT DATE(date)) AS days FROM temperatures WHERE room_id = (%s);"""
ROOM_ALL_TIME_AVG = (
    "SELECT AVG(temperature) as average FROM temperatures WHERE room_id = (%s);"
)
