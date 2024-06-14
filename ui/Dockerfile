# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file to the container
COPY requirements.txt /usr/src/app

# Install dependencies including uvicorn
RUN pip install -r requirements.txt

# Copy the frontend Streamlit script to the container
COPY . /usr/src/app

# Expose the Streamlit port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "--server.port", "8501", "app.py"]
