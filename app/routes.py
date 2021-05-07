from app import db
from flask import Blueprint
from flask import request, Blueprint, make_response
from flask import jsonify
from .models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST", "GET"])
def tasks_functions():
    if request.method == "POST":
        req_body = request.get_json()
        if "title" not in req_body or "description" not in req_body or "completed_at" not in req_body:
            return {
                "details": "Invalid data"
            }, 400
        new_task = Task(title = req_body["title"], description = req_body["description"], completed_at = req_body["completed_at"])
        db.session.add(new_task)
        db.session.commit()
        response_body = {
            "task": new_task.to_json()
        }
        return jsonify(response_body), 201

    elif request.method == "GET":
        all_tasks = Task.query.all()
        response_body = []
        for any_task in all_tasks:
            response_body.append(any_task.to_json())
        return jsonify(response_body), 200

@tasks_bp.route("/<task_id>", methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def dealing_with_id(task_id):
    a_task = Task.query.get(task_id)

    if a_task is None:
        return make_response("", 404)
    
    if request.method == "GET":
        return {
            "task": a_task.to_json()
        }, 200
    
    elif request.method == "PUT":
        info = request.get_json()

        a_task.title = info["title"]
        a_task.description = info["description"]
        a_task.completed_at = info["completed_at"]

        db.session.commit()
        return {
            "task": a_task.to_json()
        }, 200
    
    elif request.method == "DELETE":
        db.session.delete(a_task)
        db.session.commit()
        return {
            "details": f"Task {a_task.task_id} \"{a_task.title}\" successfully deleted"
        }, 200

@tasks_bp.route("/tasks?sort=asc", methods="GET")
def ascending_order():
    ascending = request.args.get("sort")
    response_body = []
    if ascending == "asc":
        new_order = Task.query.order_by(Task.title.asc())
        return new_order.to_json(), 200




#asks_bp.route("/tasks?sort=desc", methods="GET")
#def descending_order():
    # descending = request.args.get("sort")
    # response_body = []
    # if descending == "desc":