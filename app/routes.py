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
        return jsonify(tasks_response), 200  # returning the list of all tasks
        # return {task 
        #                 {"id": self.id,
    return make_response(tasks_response, 200) ## also works as #return tasks_response, 200

# Retrieve one /task/1     
@task_bp.route("/<task_id>", methods=["GET"])
def retrieve_single_task(task_id):
    task = Task.query.get(task_id)
    if task != None:
        return task.to_json_response(), 200

    return make_response('', 404)

#Update a task
@task_bp.route("/<task_id>", methods=["PUT"])  ## DO A TRY EXCEPT WITH DATAERROR
def update_task(task_id):
    task = Task.query.get(task_id)
    if task: # successful updating task
        form_data = request.get_json() # save user input form_data as json format 
        task.title = form_data["title"] # updating model? title field language?
        task.description = form_data["description"] # updating model description field for task = task_id
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return task.to_json_response(), 200
    return make_response(""), 404

# Delete a task
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):  # dict_task = task.task_to_json_response()  ==> dict_task["title"]
    task = Task.query.get(task_id) # an object, no format so if I want that, I need to jsonify? {title: "x", "description": "xyz", "completed_at": null}
    if task != None:
        db.session.delete(task)
        db.session.commit()
        details_str = f"Task {task_id} \"{task.title}\" successfully deleted"
    
        return jsonify(details = details_str), 200
        
        # {"success": True,
        #         "message": f"Task {task.id}{task.details} successfully deleted" }, 201
    return make_response(""), 404
    # {"success": False,
    #         "message": f"Task {task_id} was not found" }, 404
