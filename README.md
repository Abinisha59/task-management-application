\# Task Management Application



A simple Task Management Application built using HTML, JavaScript, Python Flask, and MySQL.



\## Features



\- Add a new task

\- Add task description

\- Select task priority

\- View all tasks

\- Mark tasks as completed

\- Delete tasks

\- Filter tasks by All, Pending, and Completed

\- Store tasks in MySQL



\## Technologies Used



\- HTML

\- JavaScript

\- Python

\- Flask

\- MySQL

\- Git

\- GitHub



\## REST APIs



| Method | Endpoint | Description |

|---|---|---|

| GET | `/api/tasks` | Get all tasks |

| POST | `/api/tasks` | Add a new task |

| PUT | `/api/tasks/<id>` | Update task status |

| DELETE | `/api/tasks/<id>` | Delete a task |



\## Database



The application uses a MySQL database named `task\_manager`.



The `tasks` table contains:



\- `id`

\- `title`

\- `description`

\- `priority`

\- `status`

\- `created\_at`



\## Project Structure



```text

task-management-application/

│

├── app.py

├── db.py

├── .gitignore

├── README.md

│

├── static/

│   └── script.js

│

└── templates/

&#x20;   └── index.html



How to Run



Create a virtual environment:



python -m venv venv



Install the required packages:



pip install flask mysql-connector-python python-dotenv



Configure the MySQL database and create the tasks table.



Create a .env file containing the MySQL password:



MYSQL\_PASSWORD=your\_mysql\_password



Run the application:



python app.py



Open the application in a browser:



http://127.0.0.1:5000

Git



This project uses Git for version control and GitHub for source-code hosting.

