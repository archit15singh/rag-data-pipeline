# Use the official Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port Prefect Orion server will run on
EXPOSE 4200

# Command to start the Prefect Orion server
CMD ["prefect", "server", "start", "--host", "0.0.0.0"]
