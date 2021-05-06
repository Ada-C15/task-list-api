from app import db
from app.models.task import Task
from flask import request
from flask import request, Blueprint, make_response
from flask import jsonify
import datetime

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@task_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_single_task(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    complete = task.completed_at_helper()  # Helper function to return boolean

    if request.method == "GET":
        return jsonify({
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": complete
            },
        }), 200
    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.is_complete = form_data["completed_at"]  # TODO: fix this

        db.session.commit()
        return jsonify({
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.completed_at_helper()
            }
        }), 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"details": f'Task {task.id} "{task.title}" successfully deleted'}), 200


@task_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        tasks = Task.query.all()
        task_response = []

        for task in tasks:
            # using jsonobject helper to create a dictionary with id, title, description, isComplete
            task_response.append(task.json_object())
        return jsonify(task_response), 200

    elif request.method == "POST":
        request_body = request.get_json()

        if "completed_at" not in request_body or "description" not in request_body or "title" not in request_body:
            return jsonify({
                "details": "Invalid data"
            }), 400

        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()
        # created a new task and changed my task objet into JSON
        # called my new_task.completed_at_helper.
        # using jsonobject helper to create a dictionary with id, title, description, isComplete
        return jsonify({"task": new_task.json_object()}), 201

        db.session.add(new_task)
        db.session.commit()


# post man testing eviroment
# # api request using url request can i find route that matches


# @task_bp.route("", methods=["POST", "GET"], strict_slashes=False)
# def post_task():
#     if request.method == "POST":
#         request_body = request.get_json()

#         if "completed_at" not in request_body or "description" not in request_body or "title" not in request_body:
#             return jsonify({
#                 "details": "Invalid data"
#             }), 400

# # This is allowing POSTMAN to test the requesting URL infomation by creating a route
#         task = Task(title=request_body["title"],
#                     description=request_body["description"],
#                     completed_at=request_body["completed_at"])
#         db.session.add(task)  # Session
#         db.session.commit()
#         complete = task.completed_at_helper()
#         return jsonify({
#             "task": {
#                 "id": 1,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": complete
#             }
#         }), 201
