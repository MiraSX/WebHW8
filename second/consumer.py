import json

import pika
from models import Contacts

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()


channel.queue_declare(queue="email_queue", durable=True)


def send(_id):
    contact = Contacts.objects(id=_id)
    contact.update(sent=True)


def callback(ch, method, properties, body):
    msg = json.loads(body)
    send(msg["id"])
    print(f"[x] Done: {msg['address']} sent to {msg['id']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="email_queue", on_message_callback=callback)

if __name__ == "__main__":
    channel.start_consuming()
