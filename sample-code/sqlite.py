import sqlite3

connection = sqlite3.connect("lecture.db")

crsr = connection.cursor()

sql_command = """CREATE TABLE emp (
    staff_number INTEGER PRIMARY KEY,
    fname VARCHAR(20),
    lname VARCHAR(30),
    gender CHAR(1),
    joining DATE);"""

crsr.execute(sql_command)

sql_command = """INSERT INTO emp VALUES (1, "Bill", "Gates", "M", "1980-10-28");"""
crsr.execute(sql_command)

connection.commit()

connection.close()