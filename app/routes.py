from flask import Blueprint, request, jsonify
from app import db
from flask.helpers import make_response
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def tasks():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"]
                    )
    db.session.add(new_task)
    db.session.commit()

    return{
        "success": True, 
        "message": f"A new task : '{new_task.title}' has been successfully created"
    }


