from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .database import Base, engine, SessionLocal
from . import models
from .models import Project

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def show_form(request: Request):
    db = SessionLocal()
    try:
        projects = db.query(Project).all()
        return templates.TemplateResponse(
            "project_assignment.html",
            {
                "request": request,
                "projects": projects
            }
        )
    finally:
        db.close()

@app.get("/projects")
def get_projects():
    db = SessionLocal()
    try:
        projects = db.query(Project).all()
        return [{"id": p.id, "name": p.name} for p in projects]
    finally:
        db.close()