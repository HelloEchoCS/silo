from openai import OpenAI
from dotenv import load_dotenv
import os

_ = load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "text-embedding-3-small"


def create_embeddings(texts: list[str] | str):
    response = client.embeddings.create(input=texts, model=MODEL)
    return [embedding.embedding for embedding in response.data]
