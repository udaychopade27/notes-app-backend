from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL loaded:", DATABASE_URL is not None)


def get_conn():
    try:
        print("Attempting DB connection...")
        conn = psycopg2.connect(
            DATABASE_URL,
            sslmode="require"
        )
        print("DB connection SUCCESS")
        return conn
    except Exception as e:
        print("DB connection FAILED:", str(e))
        raise e


@app.get("/api/notes")
def get_notes():
    try:
        print("GET /api/notes called")

        conn = get_conn()
        cur = conn.cursor()

        cur.execute("SELECT id, text FROM notes")

        rows = cur.fetchall()

        cur.close()
        conn.close()

        print("Query success, rows:", len(rows))

        return [{"id": r[0], "text": r[1]} for r in rows]

    except Exception as e:
        print("ERROR in /api/notes:", str(e))
        return {"error": str(e)}
