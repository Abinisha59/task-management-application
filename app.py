
from flask import Flask, render_template, request, jsonify
from db import get_db_connection
import mysql.connector

app = Flask(__name__)


# CREATE TABLE IF IT DOES NOT EXIST
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()
        print("Database initialized successfully")

    except mysql.connector.Error as error:
        print("Database initialization error:", error)

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


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
            SELECT *
            FROM tasks
            ORDER BY id DESC
        """)

        tasks = cursor.fetchall()

        return jsonify(tasks), 200

    except mysql.connector.Error as error:
        return jsonify({
            "error": "Database error",
            "message": str(error)
        }), 500

    except Exception as error:
        return jsonify({
            "error": "Something went wrong",
            "message": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ADD TASK
@app.route("/api/tasks", methods=["POST"])
def add_task():
    connection = None
    cursor = None

    try:
        data = request.get_json()

        # Check request body
        if not data:
            return jsonify({
                "error": "Request body cannot be empty"
            }), 400

        title = data.get("title")
        description = data.get("description")
        priority = data.get("priority")

        # Validate title
        if not title or not title.strip():
            return jsonify({
                "error": "Task title cannot be empty"
            }), 400

        # Validate description
        if not description or not description.strip():
            return jsonify({
                "error": "Task description cannot be empty"
            }), 400

        # Validate priority
        if not priority or not priority.strip():
            return jsonify({
                "error": "Priority cannot be empty"
            }), 400

        # Check allowed priority values
        if priority not in ["Low", "Medium", "High"]:
            return jsonify({
                "error": "Priority must be Low, Medium, or High"
            }), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        sql = """
            INSERT INTO tasks
            (title, description, priority, status)
            VALUES (%s, %s, %s, %s)
        """

        values = (
            title.strip(),
            description.strip(),
            priority,
            "pending"
        )

        cursor.execute(sql, values)

        connection.commit()

        task_id = cursor.lastrowid

        return jsonify({
            "message": "Task created successfully",
            "task": {
                "id": task_id,
                "title": title.strip(),
                "description": description.strip(),
                "priority": priority,
                "status": "pending"
            }
        }), 201

    except mysql.connector.Error as error:
        if connection:
            connection.rollback()

        return jsonify({
            "error": "Database error",
            "message": str(error)
        }), 500

    except Exception as error:
        if connection:
            connection.rollback()

        return jsonify({
            "error": "Something went wrong",
            "message": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# UPDATE TASK STATUS
@app.route("/api/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE tasks
            SET status = 'completed'
            WHERE id = %s
        """, (id,))

        # Check if task exists
        if cursor.rowcount == 0:
            return jsonify({
                "error": "Task not found"
            }), 404

        connection.commit()

        return jsonify({
            "message": "Task completed successfully",
            "id": id,
            "status": "completed"
        }), 200

    except mysql.connector.Error as error:
        if connection:
            connection.rollback()

        return jsonify({
            "error": "Database error",
            "message": str(error)
        }), 500

    except Exception as error:
        if connection:
            connection.rollback()

        return jsonify({
            "error": "Something went wrong",
            "message": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# DELETE TASK
@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM tasks
            WHERE id = %s
        """, (id,))

        # Check if task exists
        if cursor.rowcount == 0:
            return jsonify({
                "error": "Task not found"
            }), 404

        connection.commit()

        return jsonify({
            "message": "Task deleted successfully",
            "id": id
        }), 200

    except mysql.connector.Error as error:
        if connection:
            connection.rollback()

        return jsonify({
            "error": "Database error",
            "message": str(error)
        }), 500

    except Exception as error:
        if connection:
            connection.rollback()

        return jsonify({
            "error": "Something went wrong",
            "message": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

# INITIALIZE DATABASE
init_db()


# START APPLICATION
if __name__ == "__main__":
    app.run(debug=True)