from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
import os
import psycopg2
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://fwwwfkjoco:7O48FKA30IRL0L68$@bamaster-server.postgres.database.azure.com/bamaster-database'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    return jsonify({'sas_token': 'sp=w&st=2024-03-30T14:25:47Z&se=2024-03-30T22:25:47Z&sv=2022-11-02&sr=c&sig=j1Cvw5kaYZ7NdlLUZ%2F4nkptYNqaDyvnI7%2BjyCRYKz2A%3D'})

if __name__ == "__main__":
    app.run(debug=True)