import streamlit as st
import requests
import logging
import os

API_URL = "http://api:8000"  # Assuming FastAPI server runs locally on port 8000

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def upload_file(file_path):
    upload_url = f"{API_URL}/upload"
    try:
        with open(file_path, "rb") as f:
            files = {"fileb": f}
            logging.info(f"Uploading file: {file_path}")
            response = requests.post(upload_url, files=files)
            response.raise_for_status()
            logging.info(f"Upload response: {response.json()}")
            return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error uploading file: {e}")
        st.error(f"Error uploading file: {e}")
        return None

def download_file(filename):
    download_url = f"{API_URL}/download?filename={filename}"
    try:
        logging.info(f"Downloading file: {filename}, download_url: {download_url}")
        response = requests.get(download_url)
        response.raise_for_status()
        logging.info(f"Download response: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading file: {e}")
        st.error(f"Error downloading file: {e}")
        return None

def main():
    st.title("Video Processing App")
    st.header("Upload and Process Video")


    # # Initialize session state variables
    # if 'uploaded_file' not in st.session_state:
    #     st.session_state.uploaded_file = None
    # if 'uploaded_file_name' not in st.session_state:
    #     st.session_state.uploaded_file_name = None
    # if 'downloaded_file_path' not in st.session_state:
    #     st.session_state.downloaded_file_path = None
    # if 'upload_in_progress' not in st.session_state:
    #     st.session_state.upload_in_progress = False
    # if 'download_in_progress' not in st.session_state:
    #     st.session_state.download_in_progress = False

    # # File upload section
    # if st.session_state.uploaded_file is None:
    #     st.session_state.uploaded_file = st.file_uploader("Select a video file", type=["mp4"])

    # # Display uploaded video and upload button
    # if st.session_state.uploaded_file is not None:
    #     st.subheader("Uploaded Video")
    #     st.video(st.session_state.uploaded_file)

    #     # Upload button logic
    #     if st.button("Upload Video") and not st.session_state.upload_in_progress:
    #         st.session_state.upload_in_progress = True
    #         with st.spinner("Uploading and Processing..."):
    #             upload_dir = "/usr/src/app/uploaded_videos"
    #             os.makedirs(upload_dir, exist_ok=True)

    #             file_path = os.path.join(upload_dir, st.session_state.uploaded_file.name)
    #             with open(file_path, "wb") as f:
    #                 f.write(st.session_state.uploaded_file.getbuffer())

    #             upload_response = upload_file(file_path)
    #             if upload_response and upload_response.get("statuscode") == 200:
    #                 st.session_state.uploaded_file_name = st.session_state.uploaded_file.name
    #                 st.session_state.upload_in_progress = False
    #                 st.success("Upload and Processing Successful!")
    #             else:
    #                 st.session_state.upload_in_progress = False

    # # Download button logic
    # if st.session_state.uploaded_file_name and not st.session_state.downloaded_file_path:
    #     if st.button("Download Processed Video") and not st.session_state.download_in_progress:
    #         st.session_state.download_in_progress = True
    #         with st.spinner("Downloading Processed Video..."):
    #             filename = os.path.splitext(st.session_state.uploaded_file_name)[0]
    #             download_response = download_file(filename)
    #             if download_response and download_response.get("statuscode") == 200:
    #                 st.session_state.downloaded_file_path = download_response["file_path"]
    #                 st.session_state.download_in_progress = False
    #                 st.success("Downloaded Processed Video Successfully!")
    #             else:
    #                 st.session_state.download_in_progress = False

    # # Display video comparison side by side
    # if st.session_state.downloaded_file_path:
    #     st.subheader("Video Comparison")
    #     col1, col2 = st.columns(2)

    #     with col1:
    #         st.header("Input Video")
    #         st.video(os.path.join("/usr/src/app/uploaded_videos", st.session_state.uploaded_file_name))

    #     with col2:
    #         st.header("Processed Video")
    #         st.video(st.session_state.downloaded_file_path)

if __name__ == "__main__":
    main()
