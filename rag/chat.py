from .config import *
from .utils.chat_utils import retrieve_relevant_records, preprocessing
from .utils.history_utils import create_history, fetch_history
from .utils.prompts import *
from google.genai import types

config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION, temperature=0.2
)


def retriever(query: str, category: str):
    top_10_records = retrieve_relevant_records(
        index=index, query=query, namespace="test-namespace", category=category
    )
    retriever_text = preprocessing(top_10_records)

    return retriever_text


def text_chat(message: str, user_id: str):
    history = fetch_history(mongo_client=mongo_client, user_id=user_id)

    chat = genai_client.chats.create(config=config, history=history)

    retrieve_output = retriever(message, category="question_paper")
    prompt = CHAT_TEMPLATE.format(reference=retrieve_output, prompt=message)

    response = chat.send_message(prompt)

    updated_history = chat.get_history()

    create_history(updated_history, mongo_client, user_id)

    return response.text
