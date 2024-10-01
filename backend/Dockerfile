# Backend Dockerfile
FROM python:3.12

# Set work directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . /app

# Expose port
EXPOSE 5000

# Run the Flask app with SSL
CMD ["python", "app.py", "--certfile", "certs/server-cert.pem", "--keyfile", "certs/server-key.pem"]
