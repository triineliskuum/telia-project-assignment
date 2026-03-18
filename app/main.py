"""
Main FastAPI application.

Handles:
- routing
- form rendering (GET /)
- form submission (POST /submit)
- database interaction
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .database import Base, engine, SessionLocal
from . import models
from .models import Project, Employee

app = FastAPI()

# Mount static files (CSS and JavaScript)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="app/templates")

def render_form(request: Request, db, form_data=None, errors=None, success_message=None):
    """
    Helper function to render the form with:
    - pre-filled data
    - validation errors
    - success message
    """
    projects = db.query(Project).all()

    if form_data is None:
        form_data = {}

    if errors is None:
        errors = {}
    
    return templates.TemplateResponse(
            "project_assignment.html",
            {
                "request": request,
                "projects": projects,
                "form_data": form_data,
                "errors": errors,
                "success_message": success_message
            }
        )

@app.get("/", response_class=HTMLResponse)
def show_form(request: Request):
    """
    Renders the main form page.

    Loads all available projects from the database
    and passes them to the template.
    """
    db = SessionLocal()
    try:
        return render_form(request, db)
    finally:
        db.close()


@app.post("/submit", response_class=HTMLResponse)
def submit_form(
    request: Request,
    full_name: str = Form(""),
    email: str = Form(""),
    experience_level: str = Form(""),
    primary_stack: str = Form(""),
    preferred_duration: str = Form(""),
    additional_skills: str = Form(""),
    project_ids: list[int] = Form([])
):
    """
    Handles form submission.

    Logic:
    1. Validate input data
    2. If validation fails → return form with errors
    3. If email does not exist → create new employee
    4. If email exists → update existing employee
    5. Update selected projects (many-to-many relationship)
    """
    db = SessionLocal()
    try:
        errors = {}

        full_name = full_name.strip()
        email = email.strip()
        additional_skills = additional_skills.strip()

        form_data = {
            "full_name": full_name,
            "email": email,
            "experience_level": experience_level,
            "primary_stack": primary_stack,
            "preferred_duration": preferred_duration,
            "additional_skills": additional_skills,
            "project_ids": project_ids
        }

        # Server-side validation
        # Ensures all required fields are filled and valid
        if not full_name:
            errors["full_name"] = "Full name is required."

        if not email:
            errors["email"] = "Email address is required."
        elif "@" not in email or "." not in email:
            errors["email"] = "Please enter a valid email address."
        
        if not experience_level:
            errors["experience_level"] = "Please select your experience level."

        if not primary_stack:
            errors["primary_stack"] = "Please select your primary technology stack."

        if not preferred_duration:
            errors["preferred_duration"] = "Please select preferred project duration."

        if not project_ids:
            errors["project_ids"] = "Please select at least one project."

        if errors:
            return render_form(request, db, form_data=form_data, errors=errors)

        # Check if employee already exists (based on email)
        employee = db.query(Employee).filter(Employee.email == email).first()
        selected_projects = db.query(Project).filter(Project.id.in_(project_ids)).all()

        # Create new employee if not found
        if employee is None:
            employee = Employee(
                full_name=full_name,
                email=email,
                experience_level=experience_level,
                primary_stack=primary_stack,
                preferred_duration=preferred_duration,
                additional_skills=additional_skills,
                projects=selected_projects
            )
            db.add(employee)
            success_message = "Profile saved successfully."
        # Update existing employee if found
        else:
            employee.full_name = full_name
            employee.experience_level = experience_level
            employee.primary_stack = primary_stack
            employee.preferred_duration = preferred_duration
            employee.additional_skills = additional_skills
            # Assign selected projects to employee (replaces previous selections)
            employee.projects = selected_projects
            success_message = "Profile updated successfully."

        db.commit()
        db.refresh(employee)

        form_data = {
            "full_name": employee.full_name,
            "email": employee.email,
            "experience_level": employee.experience_level,
            "primary_stack": employee.primary_stack,
            "preferred_duration": employee.preferred_duration,
            "additional_skills": employee.additional_skills,
            "project_ids": [project.id for project in employee.projects]
        }

        return render_form(request, db, form_data=form_data, errors={}, success_message=success_message)
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