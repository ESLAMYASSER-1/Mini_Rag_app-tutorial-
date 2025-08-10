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

        self.database_dir = os.path.join(
            self.base_dir,
            "assets/database"
        )

        self.MONGODB_URL = os.getenv("MONGODB_URL")
        self.MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

        self.GENERATION_BACKEND =  os.getenv("GENERATION_BACKEND")
        self.EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND")

        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.OPENAI_API_URL = os.getenv("OPENAI_API_URL")
        self.COHERE_API_KEY = os.getenv("COHERE_API_KEY")

        self.GENERATION_MODEL_ID = os.getenv("GENERATION_MODEL_ID")
        self.EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID")
        self.EMBEDDING_MODEL_SIZE = os.getenv("EMBEDDING_MODEL_SIZE")

        self.INPUT_DEFAULT_MAX_CHARACTERS = os.getenv("INPUT_DEFAULT_MAX_CHARACTERS")
        self.GENERATION_DEFAULT_MAX_TOKENS = os.getenv("GENERATION_DEFAULT_MAX_TOKENS")
        self.GENERATION_DEFAULT_TEMPRATURE = os.getenv("GENERATION_DEFAULT_TEMPRATURE")

        self.VECTOR_DB_BACKEND = os.getenv("VECTOR_DB_BACKEND")
        self.VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH")
        self.VECTOR_DB_DISTANCE_METHOD = os.getenv("VECTOR_DB_DISTANCE_METHOD")


    def generate_random_strings(self, length:int=12):
        return "".join(random.choices(string.ascii_lowercase+string.digits, k=length))
    
    def get_database_path(self, db_name:str):

        database_path = os.path.join(
            self.database_dir,
            db_name
        )
        
        if not os.path.exists(database_path):
            os.makedirs(database_path)

        return database_path