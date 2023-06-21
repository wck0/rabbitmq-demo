#!/usr/bin/env python3
import argparse
import json
import random

import pika


RABBITMQ_USER = "landscape"
RABBITMQ_PASSWORD = "ribbityrabbit"
RABBITMQ_ADDRESS = "10.117.1.159"
RABBITMQ_PORT = 5072
RABBITMQ_VHOST = "landscape-windows-hostagent"

parser = argparse.ArgumentParser()

parser.add_argument(
    "-q", "--queue_name", type=str, help="name of the queue", default="test-uid"
)
args = parser.parse_args()

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        RABBITMQ_ADDRESS,
        RABBITMQ_PORT,
        RABBITMQ_VHOST,
        credentials,
    )
)
channel = connection.channel()
channel.queue_declare(queue=args.queue_name)

commands = [
    # {"assign_host": "with-the-most"},
    {"install": "art"},
    {"set_default": "student-loans"},
    {"shutdown_host": None},
    {"start": "me-up"},
    {"stop": "collaborate-and-listen"},
    {"uninstall": "php-server"},
]

command = random.choice(commands)
body = json.dumps(command)

channel.basic_publish(exchange="", routing_key=args.queue_name, body=body)
print(f"  Sent {body}")

connection.close()
