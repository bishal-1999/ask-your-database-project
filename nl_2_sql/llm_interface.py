from langchain_huggingface import HuggingFaceEndpoint
from decouple import config

####################################################################################################################################

HUGGINGFACEHUB_API_TOKEN = config('HUGGINGFACEHUB_API_TOKEN')  
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

def get_llm_endpoint():
    return HuggingFaceEndpoint(repo_id=repo_id, huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN)


####################################################################################################################################