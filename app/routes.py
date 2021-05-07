# Task List API Project
# Katrina Kimzey
# Cohort 15 - Paper

from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from datetime import datetime

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")

# ============== All Tasks ========================

@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        direction = request.args.get("sort")
        if direction == "asc":
            tasks = Task.query.order_by(asc("title"))
        elif direction == "desc":
            tasks = Task.query.order_by(desc("title"))
        else:
            tasks = Task.query.all()

        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "id" : task.task_id,
                "title" : task.title,
                "description" : task.description,
                "is_complete" : task.is_complete
            })

        return jsonify(tasks_response)

    elif request.method == "POST":
        request_body = request.get_json()
        try:
            new_task = Task(title=request_body["title"],
                            description=request_body["description"],
                            completed_at=request_body["completed_at"]
                            )
        except KeyError:
            return make_response({"details": "Invalid data"}, 400)

        db.session.add(new_task)
        db.session.commit()

        return make_response({"task" : new_task.to_dict()}, 201)

# ==================== Task by id ==============================

@tasks_bp.route("/<active_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(active_id):
    task = Task.query.get_or_404(active_id)

    if request.method == "GET":
        return {"task" : task.to_dict()}

    elif request.method == "PUT":
        update_data = request.get_json()

        task.title = update_data["title"]
        task.description = update_data["description"]
        task.completed_at = update_data["completed_at"]

        db.session.commit()

        return {"task" : task.to_dict()}

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"})

# ================= Task by id change completeness ======================

@tasks_bp.route("/<active_id>/mark_complete", methods=["PATCH"])
def update_to_complete(active_id):
    task = Task.query.get_or_404(active_id)

    task.completed_at = datetime.now()
    db.session.commit()

    return {"task" : task.to_dict()}

@tasks_bp.route("/<active_id>/mark_incomplete", methods=["PATCH"])
def update_to_incomplete(active_id):
    task = Task.query.get_or_404(active_id)

    task.completed_at = None
    db.session.commit()

    return {"task" : task.to_dict()}
