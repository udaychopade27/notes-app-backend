from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.get("/notes")
def get_notes():

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id,text FROM notes")

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [{"id": r[0], "text": r[1]} for r in rows]


@app.post("/notes")
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
