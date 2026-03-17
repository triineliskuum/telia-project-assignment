from bs4 import BeautifulSoup
from .database import SessionLocal, engine, Base
from .models import Project

HTML_FILE = "original/project_assignment.html"

def extract_projects_from_html(path: str):
    with open(path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")

    project_select = None

    for select in soup.find_all("select"):
        if select.has_attr("multiple"):
            project_select = select
            break

    if project_select is None:
        raise ValueError("Could not find multi-select dropdown in HTML file.")
    
    projects = []
    for option in project_select.find_all("option"):
        value = option.get("value")
        text = option.text.strip()

        if value and text:
            projects.append((int(value), text))

    return projects

def seed_projects():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        projects = extract_projects_from_html(HTML_FILE)

        for project_id, project_name in projects:
            existing_project = db.query(Project).filter(Project.id == project_id).first()
            if not existing_project:
                db.add(Project(id=project_id, name=project_name))
            
        db.commit()
        print("Projects imported successfully.")

    finally:
        db.close()

if __name__ == "__main__":
    seed_projects()