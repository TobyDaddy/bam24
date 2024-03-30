from flask import Flask, request, redirect, url_for, render_template
import os
import io
import base64
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://fwwwfkjoco:7O48FKA30IRL0L68$@bamaster-server.postgres.database.azure.com/bamaster-database'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

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

if __name__ == '__main__':
    app.run(debug=True)