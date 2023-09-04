import pika
from app.core.config import config


class MessageBroker:

    def __init__(self, queue_name):
        self.connection = None
        self.channel = None
        self.queue_name = queue_name

    def publish(self, message):
        self._connect()

        self.channel.basic_publish(
            exchange='', routing_key=self.queue_name, body=message)

        self._close()

    def start_consuming(self):
        self.channel.start_consuming()

    def _declare_consumer(self, callback):
        self._connect()

        self.channel.basic_consume(
            queue=config.RABBIT_TRAIN_QUEUE,
            on_message_callback=callback,
            auto_ack=True
        )

    def _connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=config.RABBIT_HOST,
                port=config.RABBIT_PORT,
                credentials=pika.PlainCredentials(
                    username="tubular", password="tubular"),
            )
        )

        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue=config.RABBIT_TRAIN_QUEUE, durable=True)

    def _close(self):
        self.connection.close()
