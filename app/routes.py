from app import db
from flask import request, Blueprint, make_response, jsonify
from .models.task import Task


### WAVE 1 AND 2

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
        # tasks = Task.query.order_by(Task.title.desc())  # same as above
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

    # OR try except
    try:
        request_body["is_complete"] == None
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400 
 

    new_task = Task(title = request_body["title"], \
        description = request_body["description"], \
        completed_at = request_body["completed_at"])

    db.session.add(new_task)   
    db.session.commit()  

    # we need an extra step to transfer completed_at to is_completed:
    task_dict = {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description
    }
    
    if request_body["completed_at"] == None:
        # adds key to temp dict before we can return new_task
        task_dict["is_complete"] = False
    else:
        task_dict["is_complete"] = True

    return jsonify({"task": task_dict}), 201


# define a new route to GET a specific task
@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_one_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    else:
        task_dict = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": False
        }
     
    return jsonify({"task": task_dict}), 200


# define a new route to update (PUT) one task by its id (route parameter between <>, treated as a variable):
@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_single_task(task_id):

    # check whether task_id is an int:
    if not is_int(task_id):        
        return {
            "success": False,
            "message": f"ID {task_id} must be an integer"
        }, 400
    
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    ### HOW DOES form_data WORK?
    form_data=request.get_json()
    task.title=form_data["title"]
    task.description=form_data["description"]
    task.completed_at=form_data["completed_at"]
    db.session.commit()

    task_dict = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": False                ### WHAT IF is_complete IS TRUE?
        }
    
    return jsonify({"task": task_dict}), 200


# define a new route to DELETE one book by its id (route parameter between <>, treated as a variable):
@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_task(task_id):

    # check whether book_id is an int:
    if not is_int(task_id):        # BEFORE isinstance(book_id, int):
        return {
            "success": False,
            "message": f"ID {task_id} must be an integer"
        }, 400

    task = Task.query.get(task_id)

    if task is None:
        # return make_response("", 404)   # used to render templates like HTML
        return jsonify(None), 404
   
    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task.id} "{task.title}" successfully deleted'}), 200











