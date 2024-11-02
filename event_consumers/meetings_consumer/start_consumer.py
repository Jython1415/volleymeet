import time
import pika
import sys
import os
import logging
import requests

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

MEETINGS_BACKEND_BASE_URL = "http://localhost:5001/meetings"


def send_message(json_message, channel):
    # Convert the message to a JSON string
    message = json.dumps(json_message)

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
            connected = True  # Mark as connected to proceed
        except pika.exceptions.AMQPConnectionError:
            logger.warning(f"Connection attempt failed, retrying in 5 seconds...")
            time.sleep(5)

    # Callback functions for each queue
    def handle_meeting(ch, method, properties, body):
        logger.info(f"Received meeting message: {body}")

        # Extract only participants data
        participants_data = body.get("participants")

        # Extract only attachments data
        attachments_data = body.get("attachments")

        # Extract meeting details
        title = message.get("title")
        date_time = message.get("date_time")
        location = message.get("location")
        details = message.get("details")
        meeting_id = message.get("meeting_id")

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
                MEETINGS_BACKEND_BASE_URL,
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

            send_message(participant_info, channel)        

         # Send attachment messages to attachments queue
         for attachment in attachments_data:
            attachment_info = {
                "meeting_id" = attachment.get("meeting_id")
                "attachment_url" = attachment.get("attachment_url")
                "attachment_id" = attachment.get("attachment_id")
            }

            send_message(attachment_info, channel)


    # Set up consumers
    channel.basic_consume(queue="meetings", on_message_callback=handle_meeting, auto_ack=True)

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
