#dbhelper.py
from sqlite3 import connect, Row
import sqlite3

DATABASE = 'students.db'

def get_db_connection():
    db = connect(DATABASE)
    db.row_factory = Row  
    return db

def delete_all_students():
    try:
        db = connect('students.db')
        cursor = db.cursor()

        # Delete all records in the students table
        cursor.execute("DELETE FROM students")

        # Reset the AUTOINCREMENT sequence in sqlite_sequence
        cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'students'")
        
        db.commit()
        cursor.close()
        db.close()
        return {'status': 'success', 'message': 'All students deleted and ID reset.'}
    except Exception as e:
        return {'status': 'error', 'message': f"An error occurred: {e}"}




def getall_students():
    sql = "SELECT * FROM students"
    db = connect(DATABASE)
    cursor = db.cursor()
    cursor.row_factory = Row
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

def add_student(name, image):
    try:
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        
        sql = '''INSERT INTO students (name, image) VALUES (?, ?)'''
        cursor.execute(sql, (name, image))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False  
    finally:
        connection.close()

def get_student_image_path(id):
    sql = "SELECT image FROM students WHERE id = ?"
    db = connect(DATABASE)
    cursor = db.cursor()
    cursor.row_factory = Row
    cursor.execute(sql, (id,))
    data = cursor.fetchone()
    cursor.close()
    db.close()
    return data["image"] if data else None

def student_exists(name):
    sql = "SELECT * FROM students WHERE name = ?"
    db = connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(sql, (name,))
    exists = cursor.fetchone() is not None
    cursor.close()
    db.close()
    return exists
