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

MEETINGS_BACKEND_BASE_URL = "http://localhost:80/meetings"


def send_message_participants(json_message, channel):
    # Convert the message to a JSON string
    message = json.dumps(json_message)

    # Publish the message to the "participants" queue
    channel.basic_publish(
        exchange='',
        routing_key='participants',
        body=message
    )

    logger.info(f"Sent message: {message}")

def send_message_attachments(json_message, channel):
    # Convert the message to a JSON string
    message = json.dumps(json_message)

    # Publish the message to the "participants" queue
    channel.basic_publish(
        exchange='',
        routing_key='attachments',
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
            connected = True  # Mark as connected to proceed
        except pika.exceptions.AMQPConnectionError:
            logger.warning(f"Connection attempt failed, retrying in 5 seconds...")
            time.sleep(10)

    # Callback functions for each queue
    def handle_meeting(ch, method, properties, body):
        logger.info(f"Received meeting message: {body}")

        try:
            # Decode and parse JSON body
            message_body = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            logger.error("Received a message that is not valid JSON.")
            return

        # Extract only participants data
        participants_data = message_body.get("participants")

        # Extract only attachments data
        attachments_data = message_body.get("attachments")

        # Extract meeting details
        title = message_body.get("title")
        date_time = message_body.get("date_time")
        location = message_body.get("location")
        details = message_body.get("details")
        meeting_id = message_body.get("meeting_id")

        # Prepare meeting data for POST request
        meeting_data = {
            "title": title,
            "date_time": date_time,
            "location": location,
            "details": details,
            "meeting_id": meeting_id
        }

        # Send POST request to meetings backend to create a meeting
        try:
            response = requests.post(
                url=MEETINGS_BACKEND_BASE_URL,
                json=meeting_data
            )
            response.raise_for_status()
            logger.info(f"Meeting created successfully in backend: {response.json()}")
        except requests.RequestException as e:
            logger.error(f"Failed to create meeting in backend: {e}")
            return

        # Send participant messages to participants queue
        for participant in participants_data:
            participant_info = {
                "name": participant.get("name"),
                "email": participant.get("email"),
                "participant_id": participant.get("participant_id")
            }

            send_message_participants(participant_info, channel)        

        # Send attachment messages to attachments queue
        for attachment in attachments_data:
            attachment_info = {
                "meeting_id": attachment.get("meeting_id"),
                "attachment_url": attachment.get("attachment_url"),
                "attachment_id": attachment.get("attachment_id")
            }

            send_message_attachments(attachment_info, channel)


    # Set up consumers
    channel.basic_consume(queue="meetings", on_message_callback=handle_meeting, auto_ack=True)

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
