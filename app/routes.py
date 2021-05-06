from app.models.task import Task
from app import db
from flask import request, Blueprint, make_response, Response, jsonify
from flask import Blueprint

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")
# __name___ is the second argument to the blueprint - it names the root of the path. It needs to be the same name as the file because it connects to that model file to do the things in that model file. i.e. "task" connects to task.py
# URL is saying everything thats a task ends with /tasks -- that's how to call for it

@tasks_bp.route("", methods=["POST"]) 
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["is_complete"])

    db.session.add(new_task) # adds the book to the database
    db.session.commit() # saves the task to the database

    return jsonify(new_task)
    # return make_response(f"{'Task': new_task.to_json()}",201)

# @tasks_bp.route("", methods=["GET"]) 
# def get_tasks():

    # return

# @tasks_bp.route("", methods=["PUT"]) 
# def update_tasks():

    # return

# @tasks_bp.route("", methods=["DELETE"]) 
# def delete_tasks():

    # return