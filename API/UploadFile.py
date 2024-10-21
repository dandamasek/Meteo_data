import logging
import boto3
from botocore.exceptions import ClientError
import io

def upload_file(file_obj, bucket, object_name):
    """Upload a file object to an S3 bucket

    :param file_obj: File object (e.g., BytesIO) to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name (key)
    :return: True if file was uploaded, else False
    """

    # Initialize S3 client
    s3_client = boto3.client('s3')
    
    try:
        # Upload the file content to S3 using put_object
        s3_client.put_object(Body=file_obj.getvalue(), Bucket=bucket, Key=object_name)
        print("Uploaded file {object_name}".format(object_name=object_name))
    except ClientError as e:
        logging.error(e)
        return False
    
    finally:
        # Clear the memory by closing the BytesIO object
        file_obj.close()
        
    return True
