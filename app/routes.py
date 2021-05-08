from app import db
from flask import Blueprint
from .models.task import Task
from flask import request
from flask import jsonify, make_response
from sqlalchemy import asc, desc



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

#Retrieve all /tasks  asc or desc
@task_bp.route("", methods = ["GET"], strict_slashes = False)
def retrieve_tasks_data():
    tasks = Task.query.all() 
    sort_by = request.args.get("sort") # query parameters
    tasks_response = []

    if tasks != None: 
        if sort_by != None and sort_by == "asc": # there are query params (still I need to add that part)
            tasks_asc = Task.query.order_by(Task.title.asc()).all() # this is a list in asc order
            # this puts it in the right order for the response body:
            tasks_response_asc = [task_asc.task_to_json_response() for task_asc in tasks_asc]
            return jsonify(tasks_response_asc), 200
        
        elif sort_by != None and sort_by == "desc":
            tasks_asc = Task.query.order_by(Task.title.desc()).all() # this is a list in asc order
            # this puts it in the right order for the response body:
            tasks_response_desc = [task_asc.task_to_json_response() for task_asc in tasks_asc]
            return jsonify(tasks_response_desc), 200

        for task in tasks:
            tasks_response.append(task.task_to_json_response())
            return jsonify(tasks_response), 200  # returning the list of all tasks
    return jsonify(tasks_response), 200 ## also works as #return tasks_response, 200 ### DOESN'T WORK WITH MAKE RESPONSE!!!!!

# #Retrieve all /tasks 
# @task_bp.route("", methods = ["GET"], strict_slashes = False)
# def retrieve_tasks_data():
#     # return make_response("I'm a teapot!", 418)  # to fail first test intentionally!
#     #request.method == "GET":
#     tasks = Task.query.all()
#     tasks_response = []
#     if tasks != None:
#         for task in tasks:
#             tasks_response.append(task.task_to_json_response())
#         return jsonify(tasks_response), 200  # returning the list of all tasks
#     return make_response(tasks_response, 200) ## also works as #return tasks_response, 200 

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

# Modify part of a task
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])  ## DO A TRY EXCEPT WITH DATAERROR ??
def patch_task_mark_complete(task_id):

    task = Task.query.get(task_id) ## getting the task by id (it's whole body)
    # mark_complete = request.args.get("mark_complete") # catching the mark_complete args
    # mark_incomplete = request.args.get("mark_incomplete") # catching the mark_complete args - will this throw an error?
    
    if task:  # PATCHing if: arg mark_complete specified 
                                # in URL and task id provided exists in database
                # form_data = request.get_json() # save user input form_data as json format  #this doesn't apply, there is no body
                # task.title = form_data["title"] # updating model - title field language?  ## this doesn't apply there is no ttle
        # then call function that changes it to complete
        task.set_completion() # updates it with a date in "completed_at" field
        print(task.set_completion())
        db.session.commit()
        print (task.to_json_response(), 200)
        return task.to_json_response(), 200

    return make_response(""), 404

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])  ## DO A TRY EXCEPT WITH DATAERROR ??
def patch_task_mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task:
        # task.set_completion() # updates it with a date in "completed_at" field
        task.completed_at = None
        db.session.commit()
        return task.to_json_response(), 200

    return make_response(""), 404
