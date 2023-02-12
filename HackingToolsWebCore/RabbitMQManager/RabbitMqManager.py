import json
import os
from typing import Any

import pika


class RabbitMqManager:

    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.connection = RabbitMqManager.create_connection()
        self.channel = self.connection.channel()

    @staticmethod
    def create_connection():
        url = os.getenv('RABBITMQ_URL')

        return pika.BlockingConnection(pika.URLParameters(url))

    def publish(self, queue: str, information: Any):
        self.channel.basic_publish(exchange='', routing_key=queue,
                                   body=bytes(json.dumps(information), encoding='utf-8'))

    def consume(self, queue, callback: Any):
        self.channel.basic_consume(queue=queue,
                                   auto_ack=False,
                                   on_message_callback=callback)
        self.channel.start_consuming()

    def close_connections(self):
        self.channel.close()
        self.connection.close()
