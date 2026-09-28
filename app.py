
from flask import Flask, render_template, request, jsonify
from db import get_db_connection

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# GET ALL TASKS
@app.route("/api/tasks", methods=["GET"])
def get_tasks():

    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks ORDER BY id DESC")

    tasks = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(tasks)


# ADD A TASK
@app.route("/api/tasks", methods=["POST"])
def add_task():

    data = request.get_json()

    title = data["title"]
    description = data["description"]
    priority = data["priority"]

    connection = get_db_connection()

    cursor = connection.cursor()

    sql = """
        INSERT INTO tasks (title, description, priority, status)
        VALUES (%s, %s, %s, %s)
    """

    values = (
        title,
        description,
        priority,
        "pending"
    )

    cursor.execute(sql, values)

    connection.commit()

    task_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "id": task_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "pending"
    }), 201

# UPDATE TASK STATUS
@app.route("/api/tasks/<int:id>", methods=["PUT"])
def update_task(id):

    connection = get_db_connection()

    cursor = connection.cursor()

    sql = """
        UPDATE tasks
        SET status = 'completed'
        WHERE id = %s
    """

    cursor.execute(sql, (id,))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Task completed successfully"
    })
 # DELETE TASK
@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):

    connection = get_db_connection()

    cursor = connection.cursor()

    sql = """
        DELETE FROM tasks
        WHERE id = %s
    """

    cursor.execute(sql, (id,))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Task deleted successfully"
    })   

if __name__ == "__main__":
    app.run(debug=True)

