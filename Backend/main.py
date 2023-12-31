from fastapi import FastAPI, HTTPException
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
import logging
from models import Element
from fastapi.responses import FileResponse
from pdfBuilder import build_pdf

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
        cursor.execute("SELECT * FROM categorie JOIN element ON categorie_id=categorie.id WHERE categorie_id IS NOT NULL")
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
        cursor.execute("INSERT INTO categorie (nom) VALUES ", (category))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/elements/")
async def get_elements():
    conn = sqlite3.connect('tier_list.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, titre, groupe, source, ordre FROM element WHERE category_id IS NULL ORDER BY ordre")
        elements = [{"id": row[0], "titre": row[1], "groupe": row[2], "source": row[3], "ordre": row[4]} for row in cursor.fetchall()]
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
        cursor.execute("INSERT INTO element (titre, groupe, source) VALUES (?, ?, ?)", (element.titre, element.groupe, element.source))
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

@app.put("/elements/{id}")
async def delete_element(id: int, element: Element):
    conn = sqlite3.connect('tier_list.db')
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE element SET titre=?, groupe=?, source=?, ordre=? WHERE id=?", (element.titre, element.groupe, element.source, element.ordre, id))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/download-pdf/")
async def download_pdf():
    conn = sqlite3.connect('tier_list.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT titre, groupe, source FROM element WHERE category_id IS NULL ORDER BY ordre")
        elements = [Element(titre=row[0],groupe=row[1],source=row[2]) for row in cursor.fetchall()]
        build_pdf(elements, 'tier_list.pdf')
        return FileResponse('tier_list.pdf', filename="tier_list.pdf", headers={"Content-Disposition": "attachment"})
    except Exception as e:
        logging
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    