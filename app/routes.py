from flask import Blueprint
from app.models.task import Task
from app import db 
from flask import request, Blueprint, make_response, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def handle_tasks():
    if request.method == "POST":
        request_body = request.get_json()
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["is_complete"])

    db.session.add(new_task)
    db.session.commit()
    
    return make_response(f"Task {new_task.title} successfully created",201)
    # return jsonify(new_task)