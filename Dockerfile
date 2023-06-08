# Use the official Python base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and resources
# Copy the application code
COPY app.py main.py ./

# Copy the resources
COPY resources/ ./resources

# Copy the templates
COPY templates/ ./templates

COPY tests/ ./tests

# Expose the port on which the Flask app will listen
EXPOSE 5000

# Set the environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask application
CMD ["flask", "run"]