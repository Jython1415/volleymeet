import time
import pika
import sys
import os
import logging
import json

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

def send_message(channel):
    # Construct a sample JSON message
    message_data = {
        "event": "new_participant",
        "filename": "example_file.txt",
        "size": 2048,
        "timestamp": "2024-10-29T12:00:00Z"
    }
    # Convert the message to a JSON string
    message = json.dumps(message_data)

    # Publish the message to the "participants" queue
    channel.basic_publish(
        exchange='',
        routing_key='participants',
        body=message
    )
    logger.info(f"Sent message: {message}")

def main():
    connected = False
    connection = None
    channel = None

    # Retry logic to connect to RabbitMQ
    while not connected:
        try:
            credentials = pika.PlainCredentials("rabbituser", "rabbitpassword")
            parameters = pika.ConnectionParameters("message_broker", 5672, "demo-vhost", credentials)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            logger.info("Connected to RabbitMQ")
            connected = True
        except pika.exceptions.AMQPConnectionError:
            logger.warning(f"Connection attempt failed, retrying in 5 seconds...")
            time.sleep(5)

    # Call the send_message function
    send_message(channel)

    # Clean up
    connection.close()
    logger.info("Connection closed.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Interrupted by user, exiting...')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
