from controllers import BaseController
from stores import CoHereProvider, OpenAiProvider
from stores import LLMEnums

class LLMProviderFactory(BaseController):
    def __init__(self):
        pass

    def create(self, provider):
        if provider == LLMEnums.OPENAI.value:
            return OpenAiProvider(
                            self.OPENAI_API_KEY,
                            self.OPENAI_API_URL,
                            self.INPUT_DEFAULT_MAX_CHARACTERS,
                            self.GENERATION_DEFAULT_MAX_TOKENS,
                            self.GENERATION_DEFAULT_TEMPRATURE,
                      )

        if provider == LLMEnums.COHERE.value:
            return CoHereProvider(
                            self.COHERE_API_KEY,
                            self.INPUT_DEFAULT_MAX_CHARACTERS,
                            self.GENERATION_DEFAULT_MAX_TOKENS,
                            self.GENERATION_DEFAULT_TEMPRATURE,
            )
        return None 
    