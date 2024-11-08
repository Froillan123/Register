#app.py
from flask import Flask, render_template, request, jsonify
from dbhelper import *
import base64
import os

app = Flask(__name__)

# Function to get all students
def getall_students():
    try:
        sql = "SELECT * FROM students"
        db = connect('students.db')
        cursor = db.cursor()
        cursor.row_factory = Row
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return data
    except Exception as e:
        app.logger.error(f"Error retrieving students: {e}")
        return []

# Route for the student list
@app.route('/')
def student_list():
    pagetitle = "Registration"
    return render_template('index.html', data=getall_students(), pagetitle=pagetitle)

# Add student route
@app.route('/add_student', methods=['POST'])
def add_student_route():
    name = request.form.get('name')
    image_data = request.form.get('image_data')

    if not name or not image_data:
        return jsonify({'status': 'error', 'message': 'All fields are required!'}), 400
    if student_exists(name):
        return jsonify({'status': 'error', 'message': 'Student already exists!'}), 400

    try:
        # Save the image to a file
        img_data = base64.b64decode(image_data.split(",")[1])
        image_path = f'static/images/{name}_profile.jpg'
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, 'wb') as f:
            f.write(img_data)
        db = connect('students.db')
        cursor = db.cursor()
        cursor.execute("INSERT INTO students (name, image) VALUES (?, ?)", (name, image_path))
        db.commit()
        cursor.close()
        db.close()

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        app.logger.error(f"Error adding student: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred while adding the student.'}), 500


@app.route('/delete_student', methods=['POST'])
def delete_student():
    data = request.get_json()
    student_id = data.get('idno')

    # If no student ID is provided, delete all students and reset the ID sequence
    if not student_id:
        delete_all_result = delete_all_students()
        return jsonify(delete_all_result), 200 if delete_all_result['status'] == 'success' else 500

    try:
        # Fetch the student's image path
        image_path = get_student_image_path(student_id)
        if image_path and os.path.exists(image_path):
            os.remove(image_path)  # Delete the image file from the server

        # Delete the student from the database
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        db.commit()
        cursor.close()
        db.close()

        return jsonify({'status': 'success', 'message': f'Student with ID {student_id} deleted.'}), 200
    except Exception as e:
        app.logger.error(f"Error deleting student: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred while deleting the student.'}), 500
    

if __name__ == '__main__':
    app.run(debug=True)
