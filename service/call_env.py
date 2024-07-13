import os
from dotenv import load_dotenv

load_dotenv()

class env_data : 
    def access_key() : 
        return os.getenv("ACCESS_KEY")
    
    def api_key() : 
        return os.getenv("API_KEY_OPENAI")
    
    def org_key() : 
        return os.getenv("ORG_KEY_OPENAI")