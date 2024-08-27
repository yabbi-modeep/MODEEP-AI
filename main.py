from fastapi import FastAPI, File, UploadFile, Form
import os
import uvicorn
import boto3
from botocore.exceptions import NoCredentialsError
from pydantic_settings import BaseSettings, SettingsConfigDict

app = FastAPI()

UPLOAD_DIRECTORY = "./uploaded_files/"

S3_BUCKET = os.getenv("S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...), new_filename: str = Form(None)):

    if new_filename:
        _, file_extension = os.path.splitext(file.filename)
        filename = new_filename + file_extension
    else:
        filename = file.filename

    file_path = os.path.join(UPLOAD_DIRECTORY, filename)

    for alreadyfile in os.listdir(UPLOAD_DIRECTORY):
        already_file_path = os.path.join(UPLOAD_DIRECTORY, alreadyfile)
        if os.path.isfile(already_file_path):
            os.remove(already_file_path)

    with open(file_path, "wb") as uploadfile:
        uploadfile.write(await file.read())

    try:
        s3_client.upload_file(file_path, S3_BUCKET, filename)
        s3_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{filename}"
    except NoCredentialsError:
        return {"error": "AWS credentials not found."}
    except Exception as e:
        return {"error": str(e)}

    return {"filename": filename, "file_path": file_path, "s3_url": s3_url}

if __name__ == '__main__':
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
