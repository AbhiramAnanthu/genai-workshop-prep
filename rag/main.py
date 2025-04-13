import os
from google import genai
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

client = genai.Client(api_key=google_api_key)
pc = Pinecone(api_key=pinecone_api_key)

index_name = "genai-workshop-rag"

index = pc.Index(index_name)


def get_index():
    return index
