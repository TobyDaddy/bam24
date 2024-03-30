from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
import os
import psycopg2
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://fwwwfkjoco:7O48FKA30IRL0L68$@bamaster-server.postgres.database.azure.com/bamaster-database'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

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

def generate_sas_token(account_name, account_key, container_name, blob_name):
    blob_service_client = BlobServiceClient(account_url=f"https://bamasterimge.blob.core.windows.net", credential=account_key)
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)

    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=account_key,
        container_name=container_name,
        blob_name=blob_name,
        permission=BlobSasPermissions(read=True, write=True, create=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )

    return sas_token

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    blob_name = secure_filename(file.filename)

    return jsonify({'sas_token': 'sp=w&st=2024-03-30T14:25:47Z&se=2024-03-30T22:25:47Z&sv=2022-11-02&sr=c&sig=j1Cvw5kaYZ7NdlLUZ%2F4nkptYNqaDyvnI7%2BjyCRYKz2A%3D'})

if __name__ == "__main__":
    app.run(debug=True)