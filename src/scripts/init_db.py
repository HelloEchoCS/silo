import psycopg2
import os
from dotenv import load_dotenv

_ = load_dotenv()


def connect():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USERNAME"),
    )
    return conn


def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pull_requests (
            id SERIAL PRIMARY KEY,
            url VARCHAR(255) NOT NULL,
            number INTEGER NOT NULL,
            diff_url VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            state VARCHAR(255) NOT NULL,
            body TEXT NOT NULL,
            embedding vector(1536)
        );
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
