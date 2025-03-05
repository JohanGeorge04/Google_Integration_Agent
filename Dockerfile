# Use an official Python runtime as a parent image
FROM python:3.12.4

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Expose port if needed (optional, depending on how you run the script)
EXPOSE 8080

# Define environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "langapp.py"]
