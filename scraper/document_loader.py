import os
import boto3
import datetime
from services.mongo import add_file_to_queue

async def load_document(file):
    file_extension = file.filename.split(".")[1]
    try:
        timestamp = datetime.datetime.now().isoformat().replace(':', '_')
        new_filename = f"{file.filename.split('.')[0].replace(' ', '_')}_{timestamp}.{file_extension}"
        s3 = boto3.client("s3")
        s3.upload_fileobj(file.file, os.getenv("S3_BUCKET_NAME"), new_filename)
        add_file_to_queue(new_filename)
        return {"message": "Document uploaded successfully!", "success": True}
    except Exception as e:
        return {"message": f"Something went wrong! {e}", "success": False}
