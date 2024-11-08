from langchain_community.llms.ollama import Ollama
import os 
from dotenv import load_dotenv

load_dotenv()

# host_url = os.getenv("OLLAMA_HOST")
# print(host_url)
model = os.getenv("MODEL_NAME")
base_url = os.getenv("OLLAMA_BASE_URL")
# host_url = "host.docker.internal"
llm = Ollama(model= model, base_url= base_url)
