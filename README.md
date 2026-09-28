# Task Management Application

A simple Task Management Application built using HTML, JavaScript, Python Flask, and MySQL.

## Features

* Add a new task
* Add task description
* Select task priority: Low, Medium, or High
* View all tasks
* Mark tasks as completed
* Delete tasks
* Filter tasks by All, Pending, and Completed
* Validate task input
* Handle API and database errors
* Automatically create the required database table
* Store tasks in MySQL

## Technologies Used

* HTML5
* JavaScript
* Python
* Flask
* MySQL
* Git
* GitHub

## REST API Endpoints

| Method | Endpoint          | Description              |
| ------ | ----------------- | ------------------------ |
| GET    | `/api/tasks`      | Get all tasks            |
| POST   | `/api/tasks`      | Add a new task           |
| PUT    | `/api/tasks/<id>` | Mark a task as completed |
| DELETE | `/api/tasks/<id>` | Delete a task            |

## Database

The application uses a MySQL database named `task_manager`.

The `tasks` table contains the following fields:

* `id`
* `title`
* `description`
* `priority`
* `status`
* `created_at`

The application automatically creates the `tasks` table when it starts if the table does not already exist.

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
│   └── script.js
│
└── templates/
    └── index.html
```

> **Note:** The `.env` file contains local database credentials and is excluded from Git using `.gitignore`. It should not be uploaded to GitHub.

## How to Run

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
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

### 5. Create the `.env` File

Create a `.env` file in the project root directory.

Add:

```text
MYSQL_PASSWORD=your_mysql_password
```

Replace `your_mysql_password` with your local MySQL password.

**Do not upload the `.env` file to GitHub.**

### 6. Run the Application

On Windows:

```powershell
.\venv\Scripts\python.exe app.py
```

You should see:

```text
Database initialized successfully
```

### 7. Open the Application

Open the following URL in your browser:

```text
http://127.0.0.1:5000
```

## Validation and Error Handling

The application validates task creation requests.

The following validations are included:

* Task title cannot be empty
* Task description cannot be empty
* Priority cannot be empty
* Priority must be `Low`, `Medium`, or `High`

The application also handles:

* Database errors
* Invalid API requests
* Tasks that do not exist
* Unexpected application errors

## Git and GitHub

Git is used for version control and GitHub is used to host the source code.

Example commands:

```bash
git add .
git commit -m "Update task management application"
git push
```

The project uses a `.gitignore` file to prevent unnecessary and sensitive files from being committed.

Ignored files include:

```text
venv/
__pycache__/
*.pyc
.env
.vscode/
.idea/
```

## Author

**Abinisha G**
