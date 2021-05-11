# if you see this, you're pushing from the waves-1-and-3-refactored branch!
import datetime 
from app import db
from app.models.task import Task
from sqlalchemy import asc, desc
from flask import request, Blueprint, make_response, jsonify

# Blueprint instance - groups routes that start with /tasks.
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def is_int(value):
    """
    input: a number 
    output: returns the passed-in number if it is an integer, or returns False if not
    """
    try:
        return int(value)
    except ValueError:
        return False

# Helper Function to check for valid id
def check_for_valid_id(input_id):
    """
    input: an integer ID 
    outputs: either a 400 status code if ID not found, or the passed-in ID if found
    """
    if not is_int(input_id):
        return make_response({
            "message": f"ID {input_id} must be an integer"
        }, 400)
    
    return input_id


@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_single_task(task_id):

    # Check for valid id
    check_for_valid_id(task_id)

    saved_task = Task.query.get(task_id)

    # Get One Task: No Matching Task (Returns 404 Not Found)
    if not saved_task:
        return ("", 404)

    # Get One Task: One Saved Task (Returns 200 OK)
    return make_response({"task":(saved_task.convert_to_json())}, 200)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    # Check for valid id
    check_for_valid_id(task_id)

    saved_task = Task.query.get(task_id)

    # No Matching Task (Returns 404 Not Found)
    if not saved_task:
        return ("", 404)

    # Update One Task (Returns 200 OK)
    form_data = request.get_json()

    saved_task.title = form_data["title"]
    saved_task.description = form_data["description"]
    saved_task.completed_at = form_data["completed_at"]

    db.session.commit()

    return make_response({"task":(saved_task.convert_to_json())}, 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):

    # Check for valid id
    check_for_valid_id(task_id)

    saved_task = Task.query.get(task_id)

    # No Matching Task (Returns 404 Not Found)
    if not saved_task:
        return ("", 404)

    # Delete Task: Deleting a Task (Returns 200 OK)
    db.session.delete(saved_task)
    db.session.commit()
    return {"details": f"Task {saved_task.task_id} \"{saved_task.title}\" successfully deleted"}, 200

@tasks_bp.route("/<task_id>/<mark_action>", methods=["PATCH"])
def mark_task_completeness(task_id, mark_action):

    # Check for valid id
    check_for_valid_id(task_id)

    saved_task = Task.query.get(task_id)

    if not saved_task:
        return ("", 404)

    if mark_action == "mark_complete":
        saved_task.completed_at = datetime.datetime.now()

        db.session.commit()

    elif mark_action == "mark_incomplete":
        saved_task.completed_at = None

        db.session.commit()

    return make_response({"task":(saved_task.convert_to_json())}, 200)

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def task_index():

    sort_query = request.args.get("sort")
    tasks_response = []

    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
        
    elif sort_query == "desc": 
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    for task in tasks:
        tasks_response.append(task.convert_to_json())

    return jsonify(tasks_response), 200

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():

    # Create a Task: Valid Task With null completed_at (Returns 201)
    request_body = request.get_json()

    # Create a Task: Invalid Task With Missing Data (Returns 400 Bad Request)
    if (not request_body) or ("description" not in request_body) or ("title" not in request_body) or ("completed_at" not in request_body):
        return { "details": "Invalid data"
        }, 400

    new_task = Task(title=request_body["title"],
                    description=request_body["description"], 
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task":(new_task.convert_to_json())}, 201)


    

