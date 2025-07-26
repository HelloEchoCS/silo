from openai import OpenAI
from dotenv import load_dotenv
from psycopg2.extras import RealDictRow
import os

_ = load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"


def chat(prompt: str, instructions: str):
    response = client.responses.create(
        input=prompt, model=MODEL, instructions=instructions
    )
    return response.output_text


def init_instructions(retrieved_prs: list[RealDictRow]):
    retrieval = []
    for pr in retrieved_prs:
        retrieval.append({
            "number": pr["number"] or "No number",
            "title": pr["title"] or "No title",
            "body": pr["body"] or "No description",
            "similarity": pr["similarity"] or "No similarity",
        })
    base_instruction = """
    You are a senior software engineer that answers questions about repository history.
    Answer the question based on the given most relevant pull requests, sorted by relevance. Given pull requests are in the following format:
    ```json
    {
        "number": int, // ID of the pull request
        "title": str, // Title of the pull request
        "body": str, // Description of the pull request
        "similarity": float // Relevance score of the pull request
    }
    ```
    If there are no relevant pull requests, or you find the given pull requests are not relevant, answer with "No relevant pull requests found".
    Use the relevant pull requests' titles and descriptions to answer the question.
    Organize your answer into various categories if applicable (new feature, optimizations, bug fixes, etc.), Include PR numbers you referenced in your answer.\n
    """
    retrieved_text = f"""
    Here are the most relevant pull requests:
    {retrieval}
    """
    return base_instruction + retrieved_text
