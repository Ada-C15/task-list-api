from app import db 
from .models.task import Task
from flask import request, Blueprint, make_response, Response, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
index_bp = Blueprint("index", __name__, url_prefix="/index")

####################### POST TASK CRUD - CREATE #############################
@tasks_bp.route("", methods=["POST"]) # The route usually starts with the model plural - but the tasks_bp Blueprint - is already providing the url_prefix="/books"
def create_task(): # this function will execute when a request matched the decoractor. 
    request_body = request.get_json() # the local variable request_body will hold the body contents of the HTTP request in a Python data structre (likely dictionaries, lists, and strings)
    # request.get_json() ^^ use the request object <<imported from flask>> to get information about the HTTP request - the method .get_json() grabs the part of the HTTP request_body that's in JSON format
    
    ### if request_body['title'] == None: # there is no key in the request_body called title because the client didnt input correctly
    if 'title' not in request_body.keys(): # this condition works withour the keys() function too
        response_bod = {"details": "Invalid data"}
        return jsonify(response_bod), 400
    elif 'description' not in request_body.keys():
        response_bod = {"details": "Invalid data"}
        return jsonify(response_bod), 400
    elif 'completed_at' not in request_body.keys():
        response_bod = {"details": "Invalid data"}
        return jsonify(response_bod), 400
    else:
        new_task = Task(title=request_body["title"], # We can create an instance of Task using the data in request_body. We assign this new instance to the new_task variable
                    description=request_body["description"], #use keyword arguments that match our model attribute, and access the request_body values to create the Task instance
                    completed_at=request_body["completed_at"])
        db.session.add(new_task) # adds the task model to the database
        db.session.commit() # saves the task to the database
        jsonable_new_task = new_task.to_dictionary()
    # for each endpoint - we must return the HTTP response

        return jsonify(task=jsonable_new_task), 201

# make_response() function instantiates a Response object. A Response object is generally what we want to return from Flask endpoint functions.

####################### GET ALL TASKS CRUD - READ #############################
@tasks_bp.route("", methods=["GET"]) 
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []

    for t in tasks: 
        each_task = t.to_dictionary()
        tasks_response.append(each_task)

    return jsonify(tasks_response), 200

        # tasks_response contains a list of book dictionaries. 
        # -- To turn it into a Response object, we pass it into jsonify(). This will be our common practice when --
        # -- returning a list of something because the make_response function does not handle lists.

####################### GET ONE TASK CRUD - READ #############################
# Getting a task by it's ID number
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)

    if task:
        response = {
            "id": task.id,
            "title": task.title,
            "description": task.description
        }
        return jsonify(task=task.to_dictionary()), 200
    else:
        response = None
        return jsonify(response), 404

####################### PUT TASK CRUD - UPDATE #############################
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    update_task = Task.query.get(task_id)
    if update_task is None:
        return jsonify(None), 404
    else:
        request_in_json = request.get_json()

        update_task.title = request_in_json["title"]
        update_task.description = request_in_json["description"]
        update_task.completed_at = request_in_json["completed_at"]

    # Save Action
        db.session.commit()
    
        jsonable_update_task = update_task.to_dictionary()

        return jsonify(task=jsonable_update_task), 200

    ####################### DELETE TASK CRUD - DELETE #############################
@tasks_bp.route("/<task_id>", methods=["DELETE"]) 
def delete_tasks(task_id):
    delete_task = Task.query.get(task_id)
    if delete_task is None:
        return jsonify(None), 404
    else:
    
        db.session.delete(delete_task)
        db.session.commit()
    
        response_body = f"Task {task_id} \"{delete_task.title}\" successfully deleted"


        return jsonify(details=response_body), 200
