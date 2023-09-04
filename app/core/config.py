from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_FOLDER: str = 'database'
    IMAGE_FORMAT: str = '.jpeg'
    TRAIN_IMAGES_FOLDER: str = 'train_images'
    RECOGNIZE_IMAGES_FOLDER: str = 'recognize_images'

    RABBIT_HOST: str = 'localhost'
    RABBIT_PORT: int = 5672
    RABBIT_TRAIN_QUEUE: str = 'train'

    TRAIN_FILENAME: str = 'train.yml'


config = Config()
