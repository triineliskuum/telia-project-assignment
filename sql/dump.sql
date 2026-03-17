PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE employees (
	id INTEGER NOT NULL, 
	full_name VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	experience_level VARCHAR NOT NULL, 
	primary_stack VARCHAR NOT NULL, 
	preferred_duration VARCHAR NOT NULL, 
	additional_skills VARCHAR, 
	availability_confirmed BOOLEAN, 
	PRIMARY KEY (id)
);
INSERT INTO employees VALUES(1,'karl markus','karl@gmail.com','senior','fullstack','long','user interface',0);
INSERT INTO employees VALUES(2,'karl markus','karl8@gmail.com','senior','fullstack','long','',0);
CREATE TABLE projects (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO projects VALUES(1,'Customer Portal Redesign');
INSERT INTO projects VALUES(2,'Data Pipeline Migration');
INSERT INTO projects VALUES(3,'Mobile App Enhancement');
INSERT INTO projects VALUES(4,'Internal Analytics Dashboard');
INSERT INTO projects VALUES(5,'API Gateway Implementation');
INSERT INTO projects VALUES(6,'Cloud Infrastructure Setup');
INSERT INTO projects VALUES(7,'E-commerce Platform Update');
INSERT INTO projects VALUES(8,'Reporting System Automation');
INSERT INTO projects VALUES(9,'Microservices Architecture Transition');
INSERT INTO projects VALUES(10,'Customer Data Platform Integration');
CREATE TABLE employee_projects (
	employee_id INTEGER NOT NULL, 
	project_id INTEGER NOT NULL, 
	PRIMARY KEY (employee_id, project_id), 
	FOREIGN KEY(employee_id) REFERENCES employees (id), 
	FOREIGN KEY(project_id) REFERENCES projects (id)
);
INSERT INTO employee_projects VALUES(1,10);
INSERT INTO employee_projects VALUES(2,2);
CREATE UNIQUE INDEX ix_employees_email ON employees (email);
CREATE INDEX ix_employees_id ON employees (id);
CREATE INDEX ix_projects_id ON projects (id);
COMMIT;
