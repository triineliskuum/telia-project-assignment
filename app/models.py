from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class EmployeeProject(Base):
    __tablename__ = "employee_projects"

    employee_id = Column(Integer, ForeignKey("employees.id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    experience_level = Column(String, nullable=False)
    primary_stack = Column(String, nullable=False)
    preferred_duration = Column(String, nullable=False)
    additional_skills = Column(String, nullable=True)
    availability_confirmed = Column(Boolean, default=False)

    projects = relationship(
        "Project",
        secondary="employee_projects",
        back_populates="employees"
    )


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    employees = relationship(
        "Employee",
        secondary="employee_projects",
        back_populates="projects"
    )