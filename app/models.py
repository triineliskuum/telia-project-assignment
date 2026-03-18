"""
This file defines database models (tables).

Tables:
- Employee
- Project
- EmployeeProject

The EmployeeProject table is used to create a many-to-many relationship
between employees and projects.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class EmployeeProject(Base):
    """
    Association table between employees and projects.

    This table is used for the many-to-many relationship:
    one employee can select multiple projects,
    and one project can be selected by multiple employees.
    """
    __tablename__ = "employee_projects"

    employee_id = Column(Integer, ForeignKey("employees.id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)


class Employee(Base):
    """
    Represents an employee profile submitted through the form.
    """
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    experience_level = Column(String, nullable=False)
    primary_stack = Column(String, nullable=False)
    preferred_duration = Column(String, nullable=False)
    additional_skills = Column(String, nullable=True)
    availability_confirmed = Column(Boolean, default=False)

    # Relationship to projects through the employee_projects association table
    projects = relationship(
        "Project",
        secondary="employee_projects",
        back_populates="employees"
    )


class Project(Base):
    """
    Represents a project that employees can select.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    # Relationship to employees through the employee_projects association table
    employees = relationship(
        "Employee",
        secondary="employee_projects",
        back_populates="projects"
    )