from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from config.db import conn

note = APIRouter()
templates = Jinja2Templates(directory="templates")

# Route for the About page
@note.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

# Route for the Features page
@note.get("/features", response_class=HTMLResponse)
async def features(request: Request):
    return templates.TemplateResponse("features.html", {"request": request})

@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find()
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": str(doc["_id"]),
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"]
        })
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})

@note.post("/", response_class=HTMLResponse)
async def create_note(request: Request, noteTitle: str = Form(...), noteContent: str = Form(...)):
    conn.notes.notes.insert_one({
        "title": noteTitle,
        "desc": noteContent,
        "important": False
    })
    docs = conn.notes.notes.find()
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": str(doc["_id"]),
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"]
        })
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})

@note.post("/delete/{note_id}", response_class=HTMLResponse)
async def delete_note(request: Request, note_id: str):
    conn.notes.notes.delete_one({"_id": ObjectId(note_id)})
    docs = conn.notes.notes.find()
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": str(doc["_id"]),
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"]
        })
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})

@note.post("/toggle-important/{note_id}", response_class=HTMLResponse)
async def toggle_important(request: Request, note_id: str):
    note = conn.notes.notes.find_one({"_id": ObjectId(note_id)})
    if note:
        conn.notes.notes.update_one(
            {"_id": ObjectId(note_id)},
            {"$set": {"important": not note["important"]}}
        )
    docs = conn.notes.notes.find()
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": str(doc["_id"]),
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"]
        })
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})
