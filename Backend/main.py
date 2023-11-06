from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/categories/")
async def get_categories():
    conn = sqlite3.connect('tier_list.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM category JOIN element ON category_id=category.id WHERE category_id IS NOT NULL")
        categories = cursor.fetchall()
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/categories/")
async def create_category(category: str):
    conn = sqlite3.connect('tier_list.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO category (name) VALUES ", (category))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

class Element(BaseModel):
    title : str
    group : str
    source : str

@app.get("/elements/")
async def get_elements():
    conn = sqlite3.connect('tier_list.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, title, group, source FROM element WHERE category_id IS NULL")
        elements = [{"id": row[0], "title": row[1], "group": row[2], "source": row[3]} for row in cursor.fetchall()]
        return elements
    except Exception as e:
        logging
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/elements/")
async def create_element(element: Element):
    conn = sqlite3.connect('tier_list.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO element (title, group, source) VALUES (?, ?, ?)", (element.title, element.group, element.source))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.delete("/elements/{id}")
async def delete_element(id: int):
    conn = sqlite3.connect('tier_list.db')
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM element WHERE id=?", (id,))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()