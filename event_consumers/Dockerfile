# Event_consumers Dockerfile
FROM python:3.12

# Set work directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . /app/

# Set the PYTHONPATH environment variable
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Run the consumer script
CMD ["python", "start_consumers.py"]
