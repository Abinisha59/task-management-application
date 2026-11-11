
from datetime import date
import logging

from flask import Flask, render_template, request, jsonify
from db import get_db_connection
import mysql.connector

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_PRIORITIES = {"Low", "Medium", "High"}


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


def close_resources(cursor=None, connection=None):
    if cursor is not None:
        try:
            cursor.close()
        except Exception:
            logger.exception("Failed to close database cursor")

    if connection is not None:
        try:
            connection.close()
        except Exception:
            logger.exception("Failed to close database connection")


# INITIALIZE DATABASE
def init_db():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                priority VARCHAR(20) NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'pending',
                due_date DATE NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Add due_date to an existing table if it is missing.
        cursor.execute("SHOW COLUMNS FROM tasks LIKE 'due_date'")

        if cursor.fetchone() is None:
            cursor.execute("""
                ALTER TABLE tasks
                ADD COLUMN due_date DATE NULL
            """)

        connection.commit()
        logger.info("Database initialized successfully")

    except mysql.connector.Error:
        if connection:
            try:
                connection.rollback()
            except Exception:
                logger.exception("Database initialization rollback failed")

        logger.exception("Database initialization failed")
        raise

    finally:
        close_resources(cursor, connection)


# Convert MySQL rows into JSON-friendly dictionaries.
def serialize_task(task):
    if task.get("due_date") is not None:
        task["due_date"] = task["due_date"].isoformat()

    if task.get("created_at") is not None:
        task["created_at"] = task["created_at"].isoformat(
            sep=" ", timespec="seconds"
        )

    return task


# Validate an optional date string.
def parse_due_date(value):
    if value is None or value == "":
        return None

    if not isinstance(value, str):
        raise ValueError("Due date must be a string.")

    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        raise ValueError("Enter a valid due date in YYYY-MM-DD format.")

    if parsed.isoformat() != value:
        raise ValueError("Enter a valid due date in YYYY-MM-DD format.")

    return parsed


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# GET ALL TASKS
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, title, description, priority,
                   status, due_date, created_at
            FROM tasks
            ORDER BY id DESC
        """)

        tasks = cursor.fetchall()
        return jsonify([serialize_task(task) for task in tasks]), 200

    except mysql.connector.Error:
        logger.exception("Database error while loading tasks")
        return error_response(
            "Unable to load tasks. Please try again.", 500
        )

    except Exception:
        logger.exception("Unexpected error while loading tasks")
        return error_response("An unexpected error occurred.", 500)

    finally:
        close_resources(cursor, connection)


# ADD TASK
@app.route("/api/tasks", methods=["POST"])
def add_task():
    connection = None
    cursor = None

    try:
        if not request.is_json:
            return error_response(
                "Content-Type must be application/json.", 415
            )

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return error_response(
                "Request body must be a valid JSON object.", 400
            )

        title = data.get("title")
        description = data.get("description", "")
        priority = data.get("priority")

        if not isinstance(title, str) or not title.strip():
            return error_response("Task title cannot be empty.", 400)

        title = title.strip()

        if len(title) > 255:
            return error_response(
                "Task title cannot exceed 255 characters.", 400
            )

        if description is None:
            description = ""

        if not isinstance(description, str):
            return error_response("Description must be text.", 400)

        description = description.strip()

        if not isinstance(priority, str):
            return error_response("Please select a priority.", 400)

        if priority not in ALLOWED_PRIORITIES:
            return error_response(
                "Priority must be Low, Medium, or High.", 400
            )

        try:
            due_date = parse_due_date(data.get("due_date"))
        except ValueError as error:
            return error_response(str(error), 400)

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO tasks
                (title, description, priority, status, due_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            title,
            description,
            priority,
            "pending",
            due_date
        ))

        task_id = cursor.lastrowid
        connection.commit()

        return jsonify({
            "message": "Task created successfully",
            "task": {
                "id": task_id,
                "title": title,
                "description": description,
                "priority": priority,
                "status": "pending",
                "due_date": due_date.isoformat() if due_date else None
            }
        }), 201

    except mysql.connector.Error:
        if connection:
            try:
                connection.rollback()
            except Exception:
                logger.exception("Rollback failed after database error")

        logger.exception("Database error while creating task")
        return error_response(
            "Unable to save the task. Please try again.", 500
        )

    except Exception:
        if connection:
            try:
                connection.rollback()
            except Exception:
                logger.exception("Rollback failed after unexpected error")

        logger.exception("Unexpected error while creating task")
        return error_response("An unexpected error occurred.", 500)

    finally:
        close_resources(cursor, connection)


# COMPLETE TASK
@app.route("/api/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    connection = None
    cursor = None

    if id < 1:
        return error_response("Invalid task ID.", 400)

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM tasks WHERE id = %s", (id,))

        if cursor.fetchone() is None:
            return error_response("Task not found.", 404)

        cursor.execute("""
            UPDATE tasks
            SET status = 'completed'
            WHERE id = %s
        """, (id,))

        connection.commit()

        return jsonify({
            "message": "Task completed successfully",
            "id": id,
            "status": "completed"
        }), 200

    except mysql.connector.Error:
        if connection:
            try:
                connection.rollback()
            except Exception:
                logger.exception("Rollback failed after database error")

        logger.exception("Database error while completing task")
        return error_response(
            "Unable to update the task. Please try again.", 500
        )

    except Exception:
        if connection:
            try:
                connection.rollback()
            except Exception:
                logger.exception("Rollback failed after unexpected error")

        logger.exception("Unexpected error while completing task")
        return error_response("An unexpected error occurred.", 500)

    finally:
        close_resources(cursor, connection)


# DELETE TASK
@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    connection = None
    cursor = None

    if id < 1:
        return error_response("Invalid task ID.", 400)

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))

        if cursor.rowcount == 0:
            return error_response("Task not found.", 404)

        connection.commit()

        return jsonify({
            "message": "Task deleted successfully",
            "id": id
        }), 200

    except mysql.connector.Error:
        if connection:
            try:
                connection.rollback()
            except Exception:
                logger.exception("Rollback failed after database error")

        logger.exception("Database error while deleting task")
        return error_response(
            "Unable to delete the task. Please try again.", 500
        )

    except Exception:
        if connection:
            try:
                connection.rollback()
            except Exception:
                logger.exception("Rollback failed after unexpected error")

        logger.exception("Unexpected error while deleting task")
        return error_response("An unexpected error occurred.", 500)

    finally:
        close_resources(cursor, connection)


# START APPLICATION
if __name__ == "__main__":
    try:
        init_db()
    except mysql.connector.Error:
        logger.critical("Cannot start application without database access")
        raise

    app.run(debug=True)
