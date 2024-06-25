import streamlit as st
import requests
import logging
import os
from rich.logging import RichHandler

API_URL = "http://api:8000"  # Assuming FastAPI server runs locally on port 8000

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler()],
)

def upload_file(file_path):
    upload_url = f"{API_URL}/upload"
    try:
        with open(file_path, "rb") as f:
            files = {"fileb": f}
            logging.info(f"Uploading file: {file_path}")
            response = requests.post(upload_url, files=files)
            response.raise_for_status()
            logging.debug(f"Upload response: {response.json()}")
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
        logging.debug(f"Download response: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading file: {e}")
        st.error(f"Error downloading file: {e}")
        return None

def main():
    st.set_page_config(page_title="Video Player and Live Camera Feed App", layout="wide")

    st.markdown("<h1>Video Player Feed App</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Upload a Video File</h2>", unsafe_allow_html=True)
    
    # Initialize session state variables
    if 'initial' not in st.session_state:
        st.session_state.initial = True
        logging.debug("Setting initial session state: True")

    if 'file' not in st.session_state:
        st.session_state.file = None
        logging.debug("Initializing file: None")

    if 'upload_button' not in st.session_state:
        st.session_state.upload_button = True
        logging.debug("Setting upload_button: True")

    if 'upload_in_progress' not in st.session_state:
        st.session_state.upload_in_progress = False
        logging.debug("Setting upload_in_progress: False")

    if 'download_in_progress' not in st.session_state:
        st.session_state.download_in_progress = False
        logging.debug("Setting download_in_progress: False")

    if 'downloaded_file_path' not in st.session_state:
        st.session_state.downloaded_file_path = None
        logging.debug("Initializing downloaded_file_path: None")

    if st.session_state.initial:
        # File upload section
        if st.session_state.file is None:
            st.session_state.file = st.file_uploader("Select a video file", type=["mp4"])

        # Display selected video
        if st.session_state.file:
            st.markdown("<h3>Selected Video</h3>", unsafe_allow_html=True)
            st.video(st.session_state.file)

            # Upload button logic
            if st.session_state.upload_button and not st.session_state.upload_in_progress:
                with st.container():
                    if st.button("Upload Video", key='upload_btn'):
                        st.session_state.upload_button = False
                        st.session_state.upload_in_progress = True
                        logging.debug("Upload button clicked")

        # Upload in progress
        if st.session_state.upload_in_progress:
            with st.spinner("Uploading and Processing..."):
                upload_dir = "/usr/src/app/uploaded_video"
                os.makedirs(upload_dir, exist_ok=True)

                file_path = os.path.join(upload_dir, st.session_state.file.name)
                with open(file_path, "wb") as f:
                    f.write(st.session_state.file.getbuffer())
                    logging.debug(f"File saved to: {file_path}")

                # Replace with your actual upload logic
                upload_response = upload_file(file_path)
                if upload_response and upload_response.get("status_code") == 200:
                    st.session_state.upload_in_progress = False
                    st.success("Upload and Processing Successful!")
                    logging.debug("Upload and Processing Successful")

        # Download button logic
        if not st.session_state.upload_in_progress and st.session_state.file and not st.session_state.upload_button and not st.session_state.download_in_progress:
            with st.container():
                if st.button("Download Processed Video", key='download_btn'):
                    st.session_state.download_in_progress = True
                    with st.spinner("Downloading Processed Video..."):
                        filename = os.path.splitext(st.session_state.file.name)[0]
                        download_response = download_file(filename)
                        if download_response and download_response.get("status_code") == 200:
                            st.session_state.downloaded_file_path = download_response["file_path"]
                            logging.info(f'download_response["file_path"]: {download_response["file_path"]}')
                            st.session_state.download_in_progress = False
                            st.success("Downloaded Processed Video Successfully!")
                            logging.debug("Downloaded Processed Video Successfully")

        # After download, set initial to False to show video comparison
        if st.session_state.downloaded_file_path:
            st.session_state.initial = False
            logging.debug("Setting initial: False")

    # Video comparison
    if not st.session_state.initial and st.session_state.downloaded_file_path:
        st.markdown("<h2>Video Comparison</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h3>Input Video</h3>", unsafe_allow_html=True)
            st.video(st.session_state.file)

        with col2:
            st.markdown("<h3>Processed Video</h3>", unsafe_allow_html=True)
            st.video(st.session_state.downloaded_file_path)

if __name__ == "__main__":
    main()
