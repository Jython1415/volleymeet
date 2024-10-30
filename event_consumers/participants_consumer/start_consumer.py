import time
import pika
import sys
import os
import logging

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

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
            connected = True  # Mark as connected to proceed
        except pika.exceptions.AMQPConnectionError:
            logger.warning(f"Connection attempt failed, retrying in 5 seconds...")
            time.sleep(5)

    # Callback functions
    def handle_participant(ch, method, properties, body):
        logger.info(f"Received participant message: {body}")
        # Process the participant message here

    # Set up consumer
    channel.basic_consume(queue="participants", on_message_callback=handle_participant, auto_ack=True)

    logger.info("Waiting for messages. To exit press CTRL+C")

    # Start consuming messages
    channel.start_consuming()

if __name__ == '__main__':
    try:
        time.sleep(15)
        main()
    except KeyboardInterrupt:
        logger.info('Interrupted by user, exiting...')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
