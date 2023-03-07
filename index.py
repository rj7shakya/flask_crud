from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql.cursors

# Connect to the database
# pip install pymysql
# pip install cryptography
# create database named "crud"

connection = pymysql.connect(host='localhost',
                             user='rajad',
                             password='rajad',
                             database='crud',
                             )


app = Flask(__name__)


@app.route('/')
def Index():
    cur = connection.cursor()
    cur.execute("SELECT  * FROM students")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', students=data)


@app.route('/insert', methods=['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = connection.cursor()
        cur.execute(
            "INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        connection.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    connection.commit()
    return redirect(url_for('Index'))


@app.route('/update', methods=['POST', 'GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = connection.cursor()
        cur.execute("""
               UPDATE students
               SET name=%s, email=%s, phone=%s
               WHERE id=%s
            """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        connection.commit()
        return redirect(url_for('Index'))


if __name__ == '__main__':
    # session cookies for protection against cookie data tampering.
    app.secret_key = 'super secret key'
    # It will store in the hard drive
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
