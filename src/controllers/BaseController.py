import os

class BaseController:
    def __init__(self):
        self.APP_NAME = os.getenv("APP_NAME")
        self.APP_VERSION = os.getenv("APP_VERSION")
        self.FILE_ALLOWED_TYPES = os.getenv("FILE_ALLOWED_TYPES")
        self.FILE_MAXIMUM_SIZE = os.getenv("FILE_MAXIMUM_SIZE")