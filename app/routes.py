from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("/<task_id>", methods=["GET","PUT", "DELETE"])
def get_single_task(task_id):

    task = Task.query.get(task_id)
    # With the GET, POST and DELETE request if there is nothing we output this
    if request == None or task == None:
        return jsonify(None), 404
    # This portion is the GET request for only one task
    elif request.method == "GET":
        return {"task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False}}, 200
    elif request.method == "PUT":
        # This portion is the PUT request for only one task
        request_body = request.get_json()
        task.title = request_body["title"]
        task.description = request_body["description"]
        # Save action
        db.session.commit()
        return {"task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False}}, 200
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return {
            "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
            }, 200

@tasks_bp.route("", methods=["GET"])
def tasks_index():
    # This portion is the GET request
    tasks = Task.query.all()
    if tasks == None:
        return []
    else:
        tasks_response = []
        for task in tasks:
            tasks_response.append(task.to_json())
        return jsonify(tasks_response), 200


@tasks_bp.route("", methods=["POST"])
def tasks():
    try:
        # This portion is the POST request
        request_body = request.get_json()
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()

        return make_response({
            "task": {
            "id": new_task.task_id,
            "title": request_body["title"],
            "description": request_body["description"],
            "is_complete": False
            }}, 201)
    except KeyError:
        return {
            "details": "Invalid data"}, 400


