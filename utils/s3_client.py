import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
import os
from io import BytesIO
import logging
from dotenv import load_dotenv

load_dotenv()
session = boto3.Session()
s3_client = session.client("s3")

bucket_name = os.getenv("S3_BUCKET_NAME")
def upload_file_to_s3(content, object_name):
    try:
        if not all([bucket_name, object_name]):
            return {"status": "error", "message": "Missing required parameters"}
         # converting string to bytes object
        content_bytes = BytesIO(content.encode('utf-8'))

        s3_client.upload_fileobj(content_bytes, bucket_name, object_name)

        return {"status": "success", "message": "File uploaded successfully"}
    except NoCredentialsError:
        logging.error("Credentials not available")
        return {"status": "error", "message": "Credentials not available"}

    except PartialCredentialsError:
        logging.error("Partial credentials provided")
        return {"status": "error", "message": "Partial credentials provided"}
    
    except ClientError as e:
        logging.error(f"ClientError error: {e}")
        return {"status": "error", "message": f"Client error: {e.response['Error']['Message']}"}
    
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {"status": "error", "message": f"Something went wrong: {e}"}