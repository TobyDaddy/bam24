from flask import Flask, request, redirect, url_for, render_template
import os
import io
import base64
import psycopg2
from psycopg2 import sql
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://fwwwfkjoco:7O48FKA30IRL0L68$@bamaster-server.postgres.database.azure.com/bamaster-database'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['AZURE_STORAGE_CONNECTION_STRING'] = 'DefaultEndpointsProtocol=https;AccountName=bamasterimge;AccountKey=DRwCR3smweNe/PEb0pm2slBSQFPWGhUWVgto+4g160f3y/1dXasNiEsmmz9HnbwyMK7//i731Cwn+AStJYsRRw==;EndpointSuffix=core.windows.net'
app.config['AZURE_STORAGE_CONTAINER_NAME'] = 'images'

def connect_db():
    try:
        conn = psycopg2.connect(
            user="fwwwfkjoco",
            password="7O48FKA30IRL0L68$",#"your_password",#
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

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        blob_service_client = BlobServiceClient.from_connection_string(app.config['AZURE_STORAGE_CONNECTION_STRING'])
        blob_client = blob_service_client.get_blob_client(app.config['AZURE_STORAGE_CONTAINER_NAME'], file.filename)
        blob_client.upload_blob(file)
        return 'File uploaded successfully'