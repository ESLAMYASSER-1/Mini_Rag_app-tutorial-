import os
import random
import string

class BaseController:
    def __init__(self):
        self.APP_NAME = os.getenv("APP_NAME")
        self.APP_VERSION = os.getenv("APP_VERSION")
        self.FILE_ALLOWED_TYPES = os.getenv("FILE_ALLOWED_TYPES")
        self.FILE_MAXIMUM_SIZE = os.getenv("FILE_MAXIMUM_SIZE")
        self.FILE_CHUNK_SIZE = os.getenv("FILE_CHUNK_SIZE")

        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.file_dir = os.path.join(self.base_dir, "assets/files")


    def generate_random_strings(self, length:int=12):
        return "".join(random.choices(string.ascii_lowercase+string.digits, k=length))