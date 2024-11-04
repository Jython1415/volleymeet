import time
import pika
import sys
import os
import logging
import requests
import json

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

PARTICIPANTS_BACKEND_BASE_URL = "http://localhost:80/participants"


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
            time.sleep(10)

    # Callback functions
    def handle_participant(ch, method, properties, body):
        logger.info(f"Received participant message: {body}")

        try:
            # Decode and parse JSON body
            message_body = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            logger.error("Received a message that is not valid JSON.")
            return

        # Extract participants details
        name = message_body.get("name")
        email = message_body.get("email")
        participant_id = message_body.get("participant_id")

        participant_data = {
            "name": name,
            "email": email,
            "participant_id": participant_id
        }

        # Send POST request to participants backend to create a participant
        try:
            response = requests.post(
                url=PARTICIPANTS_BACKEND_BASE_URL,
                json=participant_data
            )
            response.raise_for_status()
            logger.info(f"Participant created successfully in backend: {response.json()}")
        except requests.RequestException as e:
            logger.error(f"Failed to create participant in backend: {e}")
            return



    # Set up consumer
    channel.basic_consume(queue="participants", on_message_callback=handle_participant, auto_ack=True)

    logger.info("Waiting for messages. To exit press CTRL+C")

    # Start consuming messages
    channel.start_consuming()

if __name__ == '__main__':
    try:
        time.sleep(30)
        main()
    except KeyboardInterrupt:
        logger.info('Interrupted by user, exiting...')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
