from controllers import BaseController

class BaseDataModel(BaseController):
    def __init__(self, dbClient:object):
        self.dbClient = dbClient
        
