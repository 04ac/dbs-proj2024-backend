from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException

from models import *
from queries import *
from secret_ops import get_connection


app = FastAPI()
connection = get_connection()


@app.post("/api/room")
def create_room(room: Room):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ROOMS_TABLE)
            cursor.execute(INSERT_ROOM_RETURN_ID, (room.name,))
            room_id = cursor.fetchone()[0]
    return {"id": room_id, "message": f"Room {room.name} created."}, 201


@app.post("/api/temperature")
def add_temp(temp: Temperature):
    date = datetime.strptime(temp.date, "%m-%d-%Y %H:%M:%S") if temp.date else datetime.now(timezone.utc)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TEMPS_TABLE)
            cursor.execute(INSERT_TEMP, (temp.room_id, temp.temperature, date))
    return {"message": "Temperature added."}, 201


@app.get("/api/temperature/all")
async def get_all_temperatures():
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("SELECT * FROM temperatures")
                records = cursor.fetchall()
                if not records:
                    raise HTTPException(status_code=404, detail="No temperature records found")
                temperatures = []
                for record in records:
                    temperature_obj = {
                        "room_id": record[0],
                        "temperature": record[1],
                        "date": record[2].isoformat()  # Convert datetime object to ISO 8601 string
                    }
                    temperatures.append(temperature_obj)
                return {"temperatures": temperatures}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/average")
def get_global_avg():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GLOBAL_AVG)
            average = cursor.fetchone()[0]
            cursor.execute(GLOBAL_NUMBER_OF_DAYS)
            days = cursor.fetchone()[0]
    return {"average": round(average, 2), "days": days}


@app.get("/api/room/{room_id}")
def get_room_all(room_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(ROOM_NAME, (room_id,))
            name = cursor.fetchone()[0]
            cursor.execute(ROOM_ALL_TIME_AVG, (room_id,))
            average = cursor.fetchone()[0]
            cursor.execute(ROOM_NUMBER_OF_DAYS, (room_id,))
            days = cursor.fetchone()[0]
    return {"name": name, "average": round(average, 2), "days": days}

