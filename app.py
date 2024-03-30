from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import os
import io
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://fwwwfkjoco:7O48FKA30IRL0L68$@bamaster-server.postgres.database.azure.com/postgres'
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
            image = ImageModel(data=file.read())
            db.session.add(image)
            db.session.commit()
            return redirect(url_for('uploaded_file', id=image.id))
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

@app.route('/dbtest')
def dbtest():
    try:
        with db.engine.connect() as connection:
            result = connection.execute('SELECT version()')
            version = result.fetchone()[0]
            return f"Connected to PostgreSQL database! Version: {version}"
    except Exception as e:
        return f"Failed to connect to database: {str(e)}"

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)