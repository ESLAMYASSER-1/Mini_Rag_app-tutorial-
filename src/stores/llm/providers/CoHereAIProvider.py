from stores import LLMInterface
import cohere
import logging 
from stores import CoHereEnum, DocumentTypeEnum



class CoHereProvider(LLMInterface):
    
    def __init__(
                  self,
                  api_key:str, 
                  default_input_max_characters:int = 1000,
                  default_generation_max_output_tokens:int = 1000,
                  default_generation_temprature:float = 0.5,
    ):
        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temprature = default_generation_temprature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.ClientV2(
            api_key = self.api_key,
        )

        self.logger = logging.getLogger(__name__)
        

    def set_generation_model(
                            self, 
                            model_id:str,
                            ):
        
        self.generation_model_id = model_id

    def set_embedding_model(
                            self, 
                            model_id:str,
                            embedding_size:int,
                            ):

        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
    
    def process_text(self, text:str):
        return text.strip()[:self.default_input_max_characters]

    def generation_text(
                        self,
                        prompt:str,
                        chat_history:list =[],
                        max_output_tokens:int= None,
                        temprature:float=None,
                        ):

        if not self.client:
            self.logger.error("OpenAI Client had not Set!")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Generation Model had not Set!")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_temprature
        temprature = temprature if temprature else self.default_generation_temprature


        response = self.client.chat(
            model= self.generation_model_id,
            chat_history=chat_history,
            messages=self.process_text(prompt),
            max_tokens=max_output_tokens,
            temperature=temprature
        )

        if not response or not response.text :
            self.logger.error("Error while generating text with Cohere")
            return None
        
        return response.text


    def embed_text(
                    self,
                    text:str,
                    document_type:str = None,
                    ):

        if not self.client:
            self.logger.error("OpenAI Client had not Set!")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding Model had not Set!")
            return None
        
        input_type  = CoHereEnum.DOCUMENT.value
        if document_type == DocumentTypeEnum.QUERY.value:
            input_type = CoHereEnum.QUERY.value

        response = self.client.embed(
            model = self.embedding_model_id,
            text = [self.process_text(text)],
            input_type=input_type,
            embedding_types=['float']
        )

        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Error while embedding text with cohere")
            return None
        
        return response.embeddings.float[0]

    def construct_prompt(
                        self,
                        prompt:str,
                        role:str,
                        ):

        return {
            "role":role,
            "text":self.process_text(prompt),
        }