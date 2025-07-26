import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from .types import ProcessedPullRequestWithEmbeddings
from .embedder import create_embeddings

_ = load_dotenv()


def connect():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USERNAME"),
    )
    return conn


def insert_data(data: ProcessedPullRequestWithEmbeddings):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO pull_requests (url, number, diff_url, title, state, body, embedding)
        VALUES (%(url)s, %(number)s, %(diff_url)s, %(title)s, %(state)s, %(body)s, %(embedding)s)
    """,
        vars=data,
    )
    conn.commit()
    conn.close()


def search_similar(query: str, limit: int = 5, threshold: float = 0.4):
    conn = connect()
    embedding = create_embeddings(query)[0]
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        """
            SELECT number, title, body, 1 - (embedding <=> %s::vector) as similarity
            FROM pull_requests
            WHERE 1 - (embedding <=> %s::vector) > %s
            ORDER BY similarity DESC
            LIMIT %s
        """,
        (embedding, embedding, threshold, limit),
    )
    results = cursor.fetchall()
    conn.close()
    return results
