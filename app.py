from fastapi import FastAPI
from secret_ops import connect_mysql_db

app = FastAPI()

mydb = connect_mysql_db()


# Get all employees
@app.get("/employees")
def get_employees():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM employees")
    result = cursor.fetchall()
    return {"employees": result}


# Get an employee by ID
@app.get("/employees/{id}")
def get_employee(id: int):
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM employees WHERE id = {id}")
    result = cursor.fetchone()
    return {"employee": result}


# Add a new employee
@app.post("/employees")
def add_employee(name: str, age: int):
    cursor = mydb.cursor()
    sql = "INSERT INTO employees (name, age) VALUES (%s, %s)"
    val = (name, age)
    cursor.execute(sql, val)
    mydb.commit()
    return {"message": "Employee added successfully"}


# Delete an employee by ID
@app.delete("/employees/{id}")
def delete_employee(id: int):
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM employees WHERE id = {id}")
    mydb.commit()
    return {"message": "Employee deleted successfully"}

