# Telia project assignment

## Description
A FastAPI-based web application where employees can submit their profiles and select projects.

## Features
- Submit employee profile
- Select multiple projects
- Save to database
- Update existing profile by email
- Client-side validation (JavaScript)
- Server-side validation (FastAPI)

## Technologies
- FastAPI
- SQLAlchemy
- SQLite
- Jinja2
- HTML/CSS/JavaScript

## Setup Instructions

### 1. Clone the repository

git clone <repo-url>
cd telia-project-assignment

### 2. Create virtual environment

python -m venv venv

source venv/bin/activate   (Mac/Linux)

venv\Scripts\activate      (Windows)

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run the application

python -m uvicorn app.main:app --reload

### 5. Open in browser

http://127.0.0.1:8000

## Database

The application uses SQLite.

- Database file: project_assignment.db

- SQL dump (schema + data): sql/dump.sql

## How It Works

The form is rendered using Jinja2 templates.

Projects are loaded dynamically from the database.

When the form is submitted:

- If email does not exist → new employee is created

- If email exists → existing employee is updated

Selected projects are stored via a many-to-many relationship.

## Validation

### Client-side validation (JavaScript)

- Required fields

- Email format

- At least one project selected

### Server-side validation (FastAPI)

- Same validations enforced on backend

- Errors shown in the form

## Notes

- Email is used as a unique identifier for employees

- Form data remains filled after submission

- Error messages are displayed next to fields
