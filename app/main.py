from fastapi import FastAPI, Request, Form
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

@app.post("/submit", response_class=HTMLResponse)
def submit_form(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    experience_level: str = Form(...),
    primary_stack: str = Form(...),
    preferred_duration: str = Form(...),
    additional_skills: str = Form(""),
    project_ids: list[int] = Form(...)
):
    return HTMLResponse(f"""
        <h1>Form received successfully</h1>
        <p><strong>Full name:</strong> {full_name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Experience level:</strong> {experience_level}</p>
        <p><strong>Primary stack:</strong> {primary_stack}</p>
        <p><strong>Preferred duration:</strong> {preferred_duration}</p>
        <p><strong>Additional skills:</strong> {additional_skills}</p>
        <p><strong>Selected project IDs:</strong> {project_ids}</p>
        <p><a href="/">Back to form</a></p>     
    """)

@app.get("/projects")
def get_projects():
    db = SessionLocal()
    try:
        projects = db.query(Project).all()
        return [{"id": p.id, "name": p.name} for p in projects]
    finally:
        db.close()