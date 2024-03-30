from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # 使用SQLite数据库，你可以根据需要更改
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    new_file = Image(image=file.read())
    db.session.add(new_file)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)