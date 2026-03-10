from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os

app = FastAPI()

# Enable CORS so React frontend can call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(
        DATABASE_URL,
        sslmode="require"
    )


@app.get("/api/notes")
def get_notes():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, text FROM notes ORDER BY id DESC")

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [{"id": r[0], "text": r[1]} for r in rows]


@app.post("/api/notes")
def create_note(data: dict):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO notes(text) VALUES(%s)",
        (data["text"],)
    )

    conn.commit()

    cur.close()
    conn.close()

    return {"status": "created"}
