from app import db
from flask import request, Blueprint, jsonify
from .models.task import Task
import datetime


### WAVES 1 AND 2

# Create an endpoint specifically for tasks (all the routes start with /tasks):
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False


# define a route with default empty string for GET all tasks:
@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by("title")
    elif sort_query == "desc":
        tasks = Task.query.order_by("title desc")        # using string allows us to be more specific in our queries
        tasks = Task.query.order_by(Task.title.desc())  # same as above
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        # tasks_response.append(task.to_json()) # same as below
        if task.completed_at == None:
            tasks_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })
        else:
            tasks_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": True
            })

    return jsonify(tasks_response), 200


# define a route with default empty string for POST:
@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():  

    request_body = request.get_json()

    # if not request_body["title"] or not request_body["description"]:  # triggers key error
    if not request_body.get("title") or not request_body.get("description"):
        return jsonify({"details": "Invalid data"}), 400 

    try:
        request_body["completed_at"] == None
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400 
 

    new_task = Task(title = request_body["title"], \
        description = request_body["description"], \
        completed_at = request_body["completed_at"])

    db.session.add(new_task)   
    db.session.commit()  

    # we need an extra step to transfer completed_at to is_completed:
    task_dict = new_task.to_dict()

    return jsonify({"task": task_dict}), 201


# define a new route to GET a specific task
@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_one_task(task_id):

    if not is_int(task_id):        
        return {"message": f"ID {task_id} must be an integer"}, 400
    
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404
    else:
        task_dict = task.to_dict()
     
    return jsonify({"task": task_dict}), 200


# define a new route to update (PUT) one task by its id (route parameter between <>, treated as a variable):
@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_single_task(task_id):

    if not is_int(task_id):        
        return {"message": f"ID {task_id} must be an integer"}, 400
    
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    form_data=request.get_json()
    task.title=form_data["title"]
    task.description=form_data["description"]
    task.completed_at=form_data["completed_at"]
    db.session.commit()

    # we need an extra step to transfer completed_at to is_completed:
    task_dict = task.to_dict()
    
    return jsonify({"task": task_dict}), 200


# define a new route to DELETE one book by its id (route parameter between <>, treated as a variable):
@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_task(task_id):

    if not is_int(task_id):        
        return {"message": f"ID {task_id} must be an integer"}, 400

    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404
   
    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task.id} "{task.title}" successfully deleted'}), 200


### WAVE 3 - PATCH ROUTES

# define a new route to update (PATCH) one task by its id (route parameter between <>, treated as a variable):
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):

    if not is_int(task_id):        
        return {"message": f"ID {task_id} must be an integer"}, 400
    
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    task.completed_at=datetime.datetime.now()
    db.session.commit()

    # we need an extra step to transfer completed_at to is_completed:
    task_dict = task.to_dict()
    
    return jsonify({"task": task_dict}), 200


# define a new route to update (PATCH) one task by its id (route parameter between <>, treated as a variable):
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete(task_id):

    # check whether task_id is an int:
    if not is_int(task_id):        
        return {"message": f"ID {task_id} must be an integer"}, 400
    
    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    if task.completed_at != None:
        task.completed_at = None
        task.is_complete = False

    db.session.commit()

    task_dict = task.to_dict()
        
    return jsonify({"task": task_dict}), 200




