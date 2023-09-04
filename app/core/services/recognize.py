from app.core.interfaces.file import File
from app.core.config import config
from app.core.interfaces.message_broker import MessageBroker
from app.core.interfaces.face_regognize import FaceRecognize


class RecognizeService:

    def __init__(self):
        self.file_utils = File(base_folder=config.RECOGNIZE_IMAGES_FOLDER)
        self.train_file_utils = File(base_folder=config.TRAIN_IMAGES_FOLDER)

        self.message_broker_interface = MessageBroker(
            queue_name=config.RABBIT_TRAIN_QUEUE
        )

        self.face_recognize = FaceRecognize(
            train_folder=config.TRAIN_IMAGES_FOLDER,
            recognize_folder=config.RECOGNIZE_IMAGES_FOLDER,
            train_filename=config.TRAIN_FILENAME
        )

    async def recognize(self, image):
        filename = await self.save_image(image)
        names = self.face_recognize.recognize(filename)

        return [self.get_person_name(name) for name in names]

    async def save_image(self, image):
        return await self.file_utils.save_file(image, '', image.filename)

    def get_person_name(self, id):
        dir = self.train_file_utils.find_dir(id)
        return dir.split('/')[-1].split('-')[1]
