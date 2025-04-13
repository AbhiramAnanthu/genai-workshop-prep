from pypdf import PdfReader
import os, asyncio
from pinecone import Index
import time
from ..main import get_index


async def extract_pdf(file_name: str, docId: str) -> list[dict]:
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


# async def main():
#     file_name = (
#         "btech-cs-4-sem-computer-organisation-and-architecture-cs-it-cs202-may-2023.pdf"
#     )

#     index = get_index()
#     await upsert_data(
#         file_name=file_name, docId=1, namespace="test-namespace", index=index
#     )


# if __name__ == "__main__":
#     asyncio.run(main())
