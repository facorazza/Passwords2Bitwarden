# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create an output directory for the converted files
RUN mkdir -p /app/output

# Make sure the main script is executable
RUN chmod +x main.py

# Default command for running the script, accepts zip file and output directory as arguments
ENTRYPOINT ["python", "./main.py"]

