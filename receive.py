#!/usr/bin/env python3
import os
import sys

import pika


RABBITMQ_USER = "landscape"
RABBITMQ_PASSWORD = "landscape"
RABBITMQ_ADDRESS = "10.117.1.111"
RABBITMQ_PORT = 5672
RABBITMQ_VHOST = "landscape-hostagent"
RABBITMQ_QUEUE = "landscape-server-hostagent-task-queue"


def main():
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
    channel.queue_declare(queue=RABBITMQ_QUEUE)

    def callback(ch, method, properties, body):
        print(f"  Received {body}")

    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        auto_ack=True,
        on_message_callback=callback,
    )
    print("  Waiting for messages. CTRL-C to quit.")

    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bye")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
