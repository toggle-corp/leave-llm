import os

from dotenv import load_dotenv
from langchain_community.llms.ollama import Ollama

load_dotenv()

model = os.getenv("MODEL_NAME")
base_url = os.getenv("OLLAMA_BASE_URL")
llm = Ollama(model=model, base_url=base_url)
