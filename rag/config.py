import os
from google import genai
from dotenv import load_dotenv
from pinecone import Pinecone
from pymongo import MongoClient

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
connection_uri = os.getenv("MONGODB")


def connect_db():
    try:
        client = MongoClient(connection_uri)
        return client

    except Exception as e:
        print(f"Data base exception: {e}")


def connect_genai_client():
    try:
        client = genai.Client(api_key=google_api_key)
        return client
    except Exception as e:
        print(f"Genai exception: {e}")


def connect_pinecone():
    try:
        pc = Pinecone(api_key=pinecone_api_key)
        return pc
    except Exception as e:
        print(f"Pinecone exception: {e}")


mongo_client = connect_db()
genai_client = connect_genai_client()
pc = connect_pinecone()

index = pc.Index("genai-workshop-rag")
