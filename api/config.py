import os
import boto3
import logging

class Config:
    LOG_LEVEL = os.environ.get('LOG_LEVEL', '2')
    if LOG_LEVEL == '1':
        log_level = logging.DEBUG
    elif LOG_LEVEL == '2':
        log_level = logging.INFO
    elif LOG_LEVEL == '4':
        log_level = logging.ERROR
    elif LOG_LEVEL == '5':
        log_level = logging.CRITICAL
    else:
        log_level = logging.WARNING

    DOWNLOAD_DIR = '/usr/src/app/uploaded_videos'
    print('DOWNLOAD_DIR : ', DOWNLOAD_DIR)
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')

    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    
    INPUT_BUCKET = os.environ.get('INPUT_BUCKET')
    
    OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET')

    S3_CLIENT = boto3.client('s3',
                            aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_KEY,
                            region_name=AWS_REGION
                            )