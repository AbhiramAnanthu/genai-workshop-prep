from pypdf import PdfReader
import os, asyncio
from pinecone import Index


async def extract_pdf(file_name: str, docId: str, category: str) -> list[dict]:
    dir = "rag/data/"

    file_path = os.path.join(dir, file_name)

    try:
        if os.path.exists(file_path):
            reader = PdfReader(file_path)
            content = [
                {
                    "_id": f"{docId}#Page{index}",
                    "page_no": index,
                    "text": text.extract_text(),
                    "category": category,
                }
                for index, text in enumerate(reader.pages)
            ]

            return content
        else:
            raise FileNotFoundError()

    except FileNotFoundError as e:
        print(f"Exception: {e}")
        return None


async def upsert_data(file_name: str, docId: str, namespace: str, index: Index):
    content = await extract_pdf(file_name=file_name, docId=docId)
    if content is not None:
        index.upsert_records(namespace, content)
