from flask import Flask, render_template,request,redirect,url_for
from flask_mysqldb import MySQL

import MySQLdb.cursors
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Univalle'
app.config['MYSQL_DB'] = 'bddstudent'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def student_list_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, first_name, last_name, city, semester FROM student')
    data = cursor.fetchall()
    return json.dumps(data)

@app.route('/studentlist', methods=['GET'])
def student_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, first_name, last_name, city, semester FROM student')
    data = cursor.fetchall()
    return render_template('list.html', students=data)

@app.route('/registerstudentview', methods=['GET', 'POST'])
def registerView():
    if request.method == 'POST':
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        city = request.form['City']
        semester = request.form['Semester']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "INSERT INTO student (first_name, last_name, city, semester) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (first_name, last_name, city, semester))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('student_list'))
    return render_template('create.html')


@app.route('/editstudentview/<int:student_id>', methods=['GET', 'POST'])
def editStudentView(student_id):
    if request.method == 'POST':
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        city = request.form['City']
        semester = request.form['Semester']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "UPDATE student SET first_name=%s, last_name=%s, city=%s, semester=%s WHERE id=%s"
        cursor.execute(query, (first_name, last_name, city, semester, student_id))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('student_list'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM student WHERE id=%s"
    cursor.execute(query, (student_id,))
    student = cursor.fetchone()
    cursor.close()

    return render_template('edit.html', student=student)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
    