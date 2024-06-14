# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file to the container
COPY requirements.txt /usr/src/app

# Install dependencies including boto3
RUN pip install -r requirements.txt

# Copy the backend FastAPI script to the container
COPY . /usr/src/app

# Expose the FastAPI port
EXPOSE 8000

# Command to run the FastAPI app using uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
