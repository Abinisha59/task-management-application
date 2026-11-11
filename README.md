# Task Management Application

A simple Task Management Application built using HTML, JavaScript, Python Flask, and MySQL.

## Features

- Add new tasks with descriptions
- Select task priority: Low, Medium, or High
- View all tasks
- Mark tasks as completed
- Delete tasks
- Filter tasks by All, Pending, and Completed
- Validate task inputs
- Handle API and database errors
- Automatically create the required database table
- Store tasks in MySQL

## Technologies Used

- HTML5
- CSS3
- JavaScript
- Python
- Flask
- MySQL
- Git and GitHub

## REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/tasks` | Add a new task |
| PUT | `/api/tasks/<id>` | Update a task |
| DELETE | `/api/tasks/<id>` | Delete a task |

## Database

The application uses a MySQL database named `task_manager`.

The `tasks` table contains:

- id
- title
- description
- priority
- status
- created_at

The application automatically creates the `tasks` table when it starts if it does not already exist.

## Project Structure

```text
task-management-application/
│
├── app.py
├── db.py
├── .env
├── .gitignore
├── README.md
│
├── static/
│   ├── script.js
│   └── style.css
│
└── templates/
    └── index.html
```

**Note:** The `.env` file contains local database credentials and is excluded from Git using `.gitignore`. It should not be uploaded to GitHub.

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/Abinisha59/task-management-application.git
cd task-management-application
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Install Required Packages

```bash
pip install flask mysql-connector-python python-dotenv
```

### 4. Create the MySQL Database

Open MySQL and run:

```sql
CREATE DATABASE task_manager;
```

The application will automatically create the `tasks` table when it starts.

### 5. Configure Environment Variables

Create a `.env` file in the project root directory.

Add your MySQL password:

```text
MYSQL_PASSWORD=your_mysql_password
```

Replace the placeholder with your actual MySQL password.

**Do not upload the `.env` file to GitHub.**

### 6. Run the Application

On Windows:

```powershell
.\venv\Scripts\python.exe app.py
```

### 7. Open the Application

Open your browser and visit:

http://127.0.0.1:5000

## Validation and Error Handling

The application validates task creation requests:

- Task title cannot be empty.
- Task description cannot be empty.
- Priority cannot be empty.
- Priority must be Low, Medium, or High.

The application also handles database errors, invalid API requests, tasks that do not exist, and unexpected application errors.

## Git and GitHub

Git is used for version control, and GitHub hosts the source code.

Example commands:

```bash
git add .
git commit -m "Update task management application"
git push
```

The `.gitignore` file excludes unnecessary and sensitive files:

```text
venv/
__pycache__/
*.pyc
.env
.vscode/
.idea/
```

## Author

Abinisha G