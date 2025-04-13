# from ..config import connect_pinecone


def retrieve_relevant_records(index, query, namespace, category):
    try:
        results = index.search(
            namespace=namespace,
            query={
                "top_k": 10,
                "inputs": {
                    "text": query,
                },
                "filter": {"category": category},
            },
        )
        return results
    except Exception as e:
        print(e)


def preprocessing(query_result):
    text_list = [
        page["fields"]["text"]
        for page in query_result["result"]["hits"]
        if page["fields"]["category"] == "question_paper"
    ]
    for index, page in enumerate(text_list):
        start_index = page.find("PART")
        text_list[index] = text_list[index][start_index:]

    text = "\n".join(text_list)
    return text
