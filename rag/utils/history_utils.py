from pydantic import TypeAdapter
from google.genai import types
from pymongo import MongoClient
from ..config import connect_genai_client, connect_db
from datetime import datetime
import pytz, json

db_name = "genai-general"
collection_name = "chat-history"
history_adapter = TypeAdapter(list[types.Content])


def _get_current_ist():
    ist = pytz.timezone("Asia/Kolkata")
    time = datetime.now(ist)

    return time.strftime("%Y-%m-%d %H:%M:%S")


def _fetch_user(collection, user_id: str):
    try:
        response = collection.find_one({"user_id": user_id})
        return response
    except Exception as e:
        print(e)


def create_history(history, mongo_client: MongoClient, user_id: str):
    json_history = history_adapter.dump_json(history)

    decode_str = json_history.decode("utf-8")
    message_json = json.loads(decode_str)

    try:
        db = mongo_client[db_name]
        collection = db[collection_name]
        ist_time = _get_current_ist()

        query_filter = {"user_id": user_id}
        update_operation = {"$set": {"history": message_json, "last_updated": ist_time}}
        collection.update_one(query_filter, update_operation)
    except Exception as e:
        print(e)


def fetch_history(mongo_client: MongoClient, user_id: str):
    try:
        db = mongo_client[db_name]
        collection = db[collection_name]

        record = _fetch_user(collection, user_id)
        record_str = json.dumps(record["history"])
        history = history_adapter.validate_json(record_str)
        return history
    except Exception as e:
        print(e)

    return None
