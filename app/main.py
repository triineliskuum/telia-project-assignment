from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .database import Base, engine, SessionLocal
from . import models
from .models import Project, Employee

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
                "projects": projects,
                "form_data": {},
                "success_message": None
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
    db = SessionLocal()
    try:
        employee = db.query(Employee).filter(Employee.email == email).first()
        selected_projects = db.query(Project).filter(Project.id.in_(project_ids)).all()

        if employee is None:
            employee = Employee(
                full_name = full_name,
                email = email,
                experience_level = experience_level,
                primary_stack = primary_stack,
                preferred_duration = preferred_duration,
                additional_skills = additional_skills,
                projects = selected_projects
            )
            db.add(employee)
            success_message = "Profile saved successfully."
        else:
            employee.full_name = full_name
            employee.experience_level = experience_level
            employee.primary_stack = primary_stack
            employee.preferred_duration = preferred_duration
            employee.additional_skills = additional_skills
            employee.projects = selected_projects
            success_message = "Profile updated successfully."
        
        db.commit()
        db.refresh(employee)

        projects = db.query(Project).all()

        form_data = {
            "full_name": employee.full_name,
            "email": employee.email,
            "experience_level": employee.experience_level,
            "primary_stack": employee.primary_stack,
            "preferred_duration": employee.preferred_duration,
            "additional_skills": employee.additional_skills,
            "project_ids": [project.id for project in employee.projects]
        }

        return templates.TemplateResponse(
            "project_assignment.html",
            {
                "request": request,
                "projects": projects,
                "form_data": form_data,
                "success_message": success_message
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