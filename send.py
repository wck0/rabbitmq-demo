#!/usr/bin/env python3
import argparse
import json
import random

import pika


RABBITMQ_USER = "landscape"
RABBITMQ_PASSWORD = "landscape"
RABBITMQ_ADDRESS = "10.117.1.51"
RABBITMQ_PORT = 5672
RABBITMQ_VHOST = "landscape-hostagent"

parser = argparse.ArgumentParser()

parser.add_argument(
    "-q", "--queue_name", type=str, help="name of the queue", required=True
)
parser.add_argument(
    "-c",
    "--command",
    type=str,
    required=True,
    help="Command to send. Must be one of the following: "
    "install, set_default, shutdown_host, start, stop, uninstall",
)
parser.add_argument(
    "-i", "--instance", type=str, help="Name of the instance to target with the command"
)

VALID_COMMANDS = {
    "assign_host",
    "install",
    "set_default",
    "shutdown_host",
    "start",
    "stop",
    "uninstall",
}


def validate(args):
    if args.command not in VALID_COMMANDS:
        parser.error(
            f"{args.command} is not a valid command. Run with --help to see a list of valid commands"
        )
    if args.command == "shutdown_host" and args.instance:
        parser.error("Do not include an instance with the shutdown-host command")
    if args.command != "shutdown_host" and not args.instance:
        parser.error(f"The instance name is required for the {args.command} command")


def build_command(args):
    if args.command == "shutdown_host":
        return {"shutdown_host": None}
    if args.command == "install":
        return {"install": {"id": args.instance}}
    command = {args.command: args.instance}
    return command


args = parser.parse_args()
validate(args)

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

command = build_command(args)
body = json.dumps(command)

channel.basic_publish(exchange="", routing_key=args.queue_name, body=body)
print(f"  Sent {body}")

connection.close()
