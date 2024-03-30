from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename

    # Azure Blob Storage的连接字符串和容器名称
    connect_str = 'DefaultEndpointsProtocol=https;AccountName=bamasterimge;AccountKey=DRwCR3smweNe/PEb0pm2slBSQFPWGhUWVgto+4g160f3y/1dXasNiEsmmz9HnbwyMK7//i731Cwn+AStJYsRRw==;EndpointSuffix=core.windows.net'
    container_name = 'images'

    # 创建BlobServiceClient对象，然后获取容器客户端
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)

    # 上传文件到Azure Blob Storage
    blob_client = container_client.get_blob_client(filename)
    blob_client.upload_blob(file)

    # 生成SAS
    sas_token = generate_blob_sas(
        blob_service_client.account_name,
        container_name,
        blob_client.blob_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )

    # 返回SAS URL
    sas_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_client.blob_name}?{sas_token}"
    return {'sas_url': sas_url}

if __name__ == '__main__':
    app.run(debug=True)