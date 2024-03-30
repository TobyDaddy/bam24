from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import os
import io
import base64
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://fwwwfkjoco:7O48FKA30IRL0L68$@bamaster-server.postgres.database.azure.com/bamaster-database'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            file = request.files['file']
            data = file.read()

            conn = connect_db()
            if conn is not None:
                cur = conn.cursor()
                insert = sql.SQL('INSERT INTO image_model (data) VALUES (%s) RETURNING id')
                cur.execute(insert, (psycopg2.Binary(data),))
                id = cur.fetchone()[0]
                conn.commit()
                cur.close()
                conn.close()

                return redirect(url_for('uploaded_file', id=id))
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return render_template('error.html'), 500

    return render_template('index.html')

@app.route('/uploads/<id>')
def uploaded_file(id):
    image = ImageModel.query.get(id)
    if image is None:
        return render_template('error.html'), 404

    image_data = base64.b64encode(image.data).decode('ascii')
    return render_template('uploaded.html', img_data=image_data)

def connect_db():
    try:
        conn = psycopg2.connect(
            user="fwwwfkjoco",
            password="7O48FKA30IRL0L68$",
            host="bamaster-server.postgres.database.azure.com",
            port="5432",
            database="bamaster-database"
        )
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

@app.route('/dbtest')
def dbtest():
    conn = connect_db()
    if conn is not None:
        cur = conn.cursor()
        cur.execute('SELECT version()')
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return f"Connected to PostgreSQL database! Version: {version}"
    else:
        return "Failed to connect to database"

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)