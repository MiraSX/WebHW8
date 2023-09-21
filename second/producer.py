import json

import pika
from faker import Faker
from models import Contacts

faker = Faker("en_US")


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.exchange_declare(exchange="email_exc", exchange_type="direct")
channel.queue_declare(queue="email_queue", durable=True)
channel.queue_bind(exchange="email_exc", queue="email_queue")


def seed():
    for _ in range(5):
        Contacts(
            fullname=faker.name(), email=faker.email(), address=faker.address()
        ).save()


def main():
    contacts = Contacts.objects()

    for contact in contacts:
        msg = {
            "id": str(contact.id),
            "address": str(contact.address),
        }

        channel.basic_publish(
            exchange="email_exc",
            routing_key="email_queue",
            body=json.dumps(msg).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

    connection.close()


if __name__ == "__main__":
    seed()
    main()
