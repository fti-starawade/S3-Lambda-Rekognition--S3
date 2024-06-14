import logging
import os
import time
from config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def upload_file(file_path, filename):
    try:
        logging.info(f"Uploading file: {filename}")

        # Upload to S3 input bucket
        Config.S3_CLIENT.upload_file(file_path, Config.INPUT_BUCKET, filename)
        logging.debug(f"File uploaded to input bucket: {filename}")

        # Wait for the processed file in the output bucket
        file = filename.split('.')[0]
        processed_file_key = f"{file}"

        while True:
            response = Config.S3_CLIENT.list_objects_v2(Bucket=Config.OUTPUT_BUCKET, Prefix=processed_file_key)
            logging.debug(f"Response from S3: {response}")
            
            if 'Contents' in response:
                logging.info(f"Processed file found in output bucket: {processed_file_key}")
                break
            
            logging.info(f"Processed file not found yet, waiting...")
            time.sleep(5)  # Wait for 5 seconds before checking again

        return {"status": "Upload and processing successful", "filename": filename}

    except Exception as e:
        logging.error(f"Error in uploading file: {e}")
        return {"status": "Failed", "error": str(e)}


async def get_processed_video_path(filename: str):
    try:
        logging.info(f"Downloading processed file: {filename}")
        processed_file_key = f"{filename}_processed.mp4"
        processed_file_path = os.path.join(Config.DOWNLOAD_DIR, processed_file_key)
        
        # Download the processed file from S3 to local directory
        Config.S3_CLIENT.download_file(Config.OUTPUT_BUCKET, processed_file_key, processed_file_path)
        logging.info(f"Processed file downloaded: {processed_file_path}")
        
        return {"status": "Downloaded successfully", "file_path": processed_file_path}

    except Exception as e:
        logging.error(f"Error in downloading processed file: {e}")
        return None