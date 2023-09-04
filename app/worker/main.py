from app.core.interfaces.message_broker import MessageBroker
from app.core.services.train import TrainService
from app.core.config import config


def train_callback(ch, method, properties, body):
    train_service = TrainService()
    message = body.decode()
    train_service.train(message)


def main():
    message_broker = MessageBroker(
        queue_name=config.RABBIT_TRAIN_QUEUE
    )

    message_broker._declare_consumer(train_callback)

    message_broker.start_consuming()


if __name__ == '__main__':
    main()
