# if you see this, you're pushing from the waves-1-2-3-refactored branch!
import datetime 
from app import db
from app.models.task import Task
from sqlalchemy import asc, desc
from flask import request, Blueprint, make_response, jsonify


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def is_int(input_id):
    """
    input: the input id value
    output: tries to return an integer form of input value; if that raises an error, it returns False
    """
    try:
        return int(input_id)
    except ValueError:
        return False
    
# Get One Saved Task (Successful = Returns 200 OK); No Matching Task Returns 404 Not Found
@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_single_task(task_id):

    # Note to grader: I tried to create a helper function or class method that would check for an existing, integer task ID AND query a task with that ID, but couldn't get it to work. I realize the following code is repeated in almost every function definition here - just couldn't figure out a workaround!! 

    # Check for valid id
    if not is_int(task_id):
        return {
            "message": f"ID {task_id} must be an integer",
            "success": False
        }, 400

    saved_task = Task.query.get(task_id)

    if not saved_task:
        return ("", 404)

    return make_response({"task":(saved_task.convert_to_json())}, 200)

# Update One Task (Successful = Returns 200 OK); No Matching Task Returns 404 Not Found
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    # Check for valid id
    if not is_int(task_id):
        return {
            "message": f"ID {task_id} must be an integer",
            "success": False
        }, 400

    saved_task = Task.query.get(task_id)

    if not saved_task:
        return ("", 404)

    
    form_data = request.get_json()

    saved_task.title = form_data["title"]
    saved_task.description = form_data["description"]
    saved_task.completed_at = form_data["completed_at"]

    db.session.commit()

    return make_response({"task":(saved_task.convert_to_json())}, 200)

# Delete One Task (Successful = Returns 200 OK); No Matching Task Returns 404 Not Found
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):

    # Check for valid id
    if not is_int(task_id):
        return {
            "message": f"ID {task_id} must be an integer",
            "success": False
        }, 400

    saved_task = Task.query.get(task_id)

    if not saved_task:
        return ("", 404)

    db.session.delete(saved_task)
    db.session.commit()
    return {"details": f"Task {saved_task.task_id} \"{saved_task.title}\" successfully deleted"}, 200

# Allows client to send a patch request to mark a task as complete or incomplete (Successful = Returns 200 OK); No Matching Task Returns 404 Not Found
@tasks_bp.route("/<task_id>/<mark_action>", methods=["PATCH"])
def mark_task_completeness(task_id, mark_action):

    # Check for valid id
    if not is_int(task_id):
        return {
            "message": f"ID {task_id} must be an integer",
            "success": False
        }, 400

    saved_task = Task.query.get(task_id)

    if not saved_task:
        return ("", 404)

    if mark_action == "mark_complete":
        # Updates Task instance "completed_at" attribute with current time, in datetime format  
        saved_task.completed_at = datetime.datetime.now()

        db.session.commit()

    elif mark_action == "mark_incomplete":
        saved_task.completed_at = None

        db.session.commit()

    return make_response({"task":(saved_task.convert_to_json())}, 200)

# Get All Saved Tasks (Successful = Returns 200 OK); No Saved Tasks still returns 200 OK
@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def task_index():

    # Gets query param sorting direction from query key "sort" and assigns to a variable
    query_sort_direction = request.args.get("sort")
    tasks_response = []

    # Queries a list of all Task instances in ascending order by title
    if query_sort_direction == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    
    # Queries a list of all Task instances in descending order by title
    elif query_sort_direction == "desc": 
        tasks = Task.query.order_by(desc(Task.title))

    # If no query param "sort" key is passed in, just queries a list of all Task instances, which defaults to ascending order by ID number 
    else:
        tasks = Task.query.all()

    # Converts each task dictionary to JSON and appends to tasks_response list 
    for task in tasks:
        tasks_response.append(task.convert_to_json())

    # Converts tasks_response list into a JSON response object, returns it
    return jsonify(tasks_response), 200

# Create Valid Task With null completed_at (Successful = Returns 201); Attempt to create Invalid Task With Missing Data Returns 400 Bad Request
@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():

    request_body = request.get_json()

    if (not request_body) or ("description" not in request_body) or ("title" not in request_body) or ("completed_at" not in request_body):
        return { "details": "Invalid data"
        }, 400

    new_task = Task(title=request_body["title"],
                    description=request_body["description"], 
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task":(new_task.convert_to_json())}, 201)


    

