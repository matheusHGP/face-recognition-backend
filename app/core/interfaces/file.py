import os
import glob
import shortuuid
import aiofiles
from app.core.config import config


class File:
    def __init__(self, base_folder):
        self.base_folder = os.path.join(config.DATABASE_FOLDER, base_folder)
        self.create_dir()

    async def save_file(self, file, path, name):
        name = self._generate_unique_filename(name)
        path = os.path.join(self.base_folder, path)

        async with aiofiles.open(os.path.join(path, name), 'wb') as out_file:
            while content := await file.read(1024):
                await out_file.write(content)

        return name

    def create_dir(self, path=None):
        create_path = self.base_folder
        if path:
            create_path = os.path.join(create_path, path)

        if not os.path.isdir(create_path):
            os.mkdir(create_path)

    def find_dir(self, name):
        dir = glob.glob(os.path.join(self.base_folder, f'*{name}*'))
        if len(dir):
            return dir[0]
        return None

    def _generate_unique_filename(self, name):
        return self._generate_uuid() + '-' + name

    def _generate_unique_foldername(self, name=None):
        unique = self._generate_uuid()
        if name:
            unique = unique + '-' + name
        return unique

    def _generate_uuid(self):
        return str(shortuuid.ShortUUID(alphabet="0123456789").random(length=8))
