from app import db
from flask import Blueprint
from .models.task import Task
from flask import request
from flask import jsonify, make_response

# creating instance of the class, first arg is name of app's module
task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#create a task with null completed at
@task_bp.route("", methods = ["POST"], strict_slashes = False)
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task(title=request_body["title"],
                description=request_body["description"],
                completed_at = request_body["completed_at"])

        db.session.add(new_task) # "adds model to the db"
        db.session.commit() # does the action above
        return new_task.to_json_response(), 201
    except KeyError:
        return {"details": "Invalid data"}, 400

#Retrieve all /tasks  
@task_bp.route("", methods = ["GET"], strict_slashes = False)
def retrieve_tasks_data():
    # return make_response("I'm a teapot!", 418)  # to fail first test intentionally!
    #request.method == "GET":
    tasks = Task.query.all()
    tasks_response = []
    if tasks != None:
        for task in tasks:
            tasks_response.append(task.task_to_json_response())
        return jsonify(tasks_response), 200  # returning the list of all planets
        # return {task 
        #                 {"id": self.id,
    return tasks_response, 200

# Retrieve one /task/1     
@task_bp.route("/<task_id>", methods=["GET"])
def retrieve_single_task(task_id):
    task = Task.query.get(task_id)
    if task != None:
        return task.to_json_response(), 200

    return make_response('', 404)