from flask import Flask, jsonify, request, send_from_directory  # Added request import
from flask_pydantic import validate

from db_manager import DatabaseManager
from models import Task, TaskCreate, TaskList, TaskUpdate

app = Flask(__name__)
db = DatabaseManager()


# Route to serve the main page
@app.route("/")
def index():
    return send_from_directory("static", "index.html")


# Route to serve static files
@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)


@app.route("/tasks", methods=["POST"])
@validate()
def create_task(body: TaskCreate):
    """Create a new task"""
    task_data = body.model_dump()
    task = db.create_task(task_data)
    return jsonify(Task(**task).model_dump()), 201


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id: int):
    """Get a specific task"""
    task = db.get_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(Task(**task).model_dump())


@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Get all tasks"""
    # Get completion status from query parameter
    completed = request.args.get("completed")
    if completed is not None:
        completed = completed.lower() == "true"
        tasks = db.get_all_tasks(completed=completed)
    else:
        tasks = db.get_all_tasks()

    return jsonify(
        TaskList(
            tasks=[Task(**task) for task in tasks], total_count=len(tasks)
        ).model_dump()
    )


@app.route("/tasks/completed", methods=["GET"])
def get_completed_tasks():
    """Get all completed tasks"""
    tasks = db.get_completed_tasks()
    return jsonify(
        TaskList(
            tasks=[Task(**task) for task in tasks], total_count=len(tasks)
        ).model_dump()
    )


@app.route("/tasks/<int:task_id>", methods=["PUT"])
@validate()
def update_task(task_id: int, body: TaskUpdate):
    """Update a task"""
    task_data = body.model_dump(exclude_unset=True)
    task = db.update_task(task_id, task_data)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(Task(**task).model_dump())


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    """Delete a task"""
    if db.delete_task(task_id):
        return "", 204
    return jsonify({"error": "Task not found"}), 404


@app.errorhandler(422)
def handle_validation_error(err):
    """Handle validation errors"""
    return jsonify({"errors": err.description}), 422


if __name__ == "__main__":
    app.run(debug=True)
