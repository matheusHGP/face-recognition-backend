from app.core.interfaces.file import File
from app.core.config import config
from app.core.interfaces.message_broker import MessageBroker
from app.core.interfaces.face_regognize import FaceRecognize


class TrainService:

    def __init__(self):
        self.file_utils = File(base_folder=config.TRAIN_IMAGES_FOLDER)

        self.message_broker_interface = MessageBroker(
            queue_name=config.RABBIT_TRAIN_QUEUE
        )

        self.face_recognize = FaceRecognize(
            train_folder=config.TRAIN_IMAGES_FOLDER,
            recognize_folder=config.RECOGNIZE_IMAGES_FOLDER,
            train_filename=config.TRAIN_FILENAME
        )

    def train(self, folder_name):
        self.face_recognize.train_or_update_model(
            folder_name
        )

    async def upload_images(self, person_name, images):
        folder_name = await self.save_files(person_name, images)

        await self.queue_messages([folder_name])

    async def save_files(self, person_name, images):
        folder = self.file_utils._generate_unique_foldername(person_name)
        self.file_utils.create_dir(folder)

        for image in images:
            await self.file_utils.save_file(image, folder, image.filename)

        return folder

    async def queue_messages(self, messages):
        for message in messages:
            self.message_broker_interface.publish(message)
