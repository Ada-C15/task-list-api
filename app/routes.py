from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods = ["POST"])
def handle_tasks():
    if request.method == "POST":
        request_body = request.get_json()
        new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=["completed_at"])
        db.session.add(new_task)
        db.session.commit()

        return make_response(
        { "task": {
            "id": 1,
            "title": "A Brand New Task",
            "description": "Test Description",
            "is_complete": False
            }
}, 201)