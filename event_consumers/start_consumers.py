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

    # Callback functions for each queue
    def handle_meeting(ch, method, properties, body):
        logger.info(f"Received meeting message: {body}")
        # Process the meeting message here

    def handle_attachment(ch, method, properties, body):
        logger.info(f"Received attachment message: {body}")
        # Process the attachment message here

    def handle_participant(ch, method, properties, body):
        logger.info(f"Received participant message: {body}")
        # Process the participant message here

    # Set up consumers for each queue
    channel.basic_consume(queue="meetings", on_message_callback=handle_meeting, auto_ack=True)
    channel.basic_consume(queue="attachments", on_message_callback=handle_attachment, auto_ack=True)
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
