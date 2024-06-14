import uvicorn
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
import logging
from config import Config
from resolver import upload_file, get_processed_video_path
from rich.logging import RichHandler

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler()],
)

@app.post("/upload")
async def upload_video(fileb: UploadFile = File(...)):
    try:
        logging.info(f"Uploading Request for file: {fileb.filename}")
        file_path = os.path.join(Config.DOWNLOAD_DIR, fileb.filename)
        
        # Save the uploaded file to the specified file path
        with open(file_path, "wb") as f:
            f.write(fileb.file.read())
        
        # Call the upload_file function from resolver module to handle further processing
        response = await upload_file(file_path, fileb.filename)

        # Check if upload and processing were successful
        if response and response.get("status") == "Upload and processing successful":
            # Return success response
            return {"status": "Upload and processing successful", "filename": fileb.filename, "status_code": 200}
        else:
            # Return error response if upload or processing failed
            raise HTTPException(status_code=500, detail="Upload or processing failed")

    except Exception as e:
        logging.error(f"Error in uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download")
async def download_video(filename: str):
    try:
        logging.info(f"Download Request for file: {filename}")
        
        # Call the resolver function to get the processed video path
        response = await get_processed_video_path(filename)
        
        if response and response.get("file_path"):
            # Return success response with the file path
            return {"status": "Downloaded successfully", "file_path": response["file_path"], "status_code": 200}
        else:
            # Return error response if file path is not found or other errors occur
            raise HTTPException(status_code=404, detail="Processed video not found")

    except Exception as e:
        logging.error(f"Error in downloading processed file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
