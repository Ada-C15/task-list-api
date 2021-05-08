import datetime 
from app import db
from app.models.task import Task
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from flask import request, Blueprint, make_response, jsonify

# Blueprint instance - groups routes that start with /tasks.
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# Identify the following based on the given prompt:

#    - the HTTP Method: 
#    - Endpoint:  
#    - Request body
#    - Appropriate successful response status code (and response body, if needed): 

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):

    saved_task = Task.query.get(task_id)

    # Get OR Update OR Delete One Task: No Matching Task (Returns 404 Not Found)
    if not saved_task:
        return ("", 404)

    # Get One Task: One Saved Task (Returns 200 OK)
    if request.method == "GET":

        return { "task": {
            "id": saved_task.task_id,
            "title": saved_task.title,
            "description": saved_task.description,
            "is_complete": bool(saved_task.completed_at)
        }}, 200

    # Update One Task (Returns 200 OK)
    elif request.method == "PUT":
        form_data = request.get_json()

        saved_task.title = form_data["title"]
        saved_task.description = form_data["description"]
        saved_task.completed_at = form_data["completed_at"]

        db.session.commit()

        return { "task": {
            "id": saved_task.task_id,
            "title": saved_task.title,
            "description": saved_task.description,
            "is_complete": bool(saved_task.completed_at)
        }}, 200



    # Delete Task: Deleting a Task (Returns 200 OK)
    elif request.method == "DELETE":
        db.session.delete(saved_task)
        db.session.commit()
        return {"details": f"Task {saved_task.task_id} \"{saved_task.title}\" successfully deleted"}, 200

@tasks_bp.route("/<task_id>/<mark_action>", methods=["PATCH"])
def make_patch_request(task_id, mark_action):

    saved_task = Task.query.get(task_id)

    if not saved_task:
        return ("", 404)

    if request.method == "PATCH":
        if mark_action == "mark_complete":

            saved_task.completed_at = datetime.datetime.now()

            db.session.commit()

        elif mark_action == "mark_incomplete":

            saved_task.completed_at = None

            db.session.commit()

        return { "task": {
                "id": saved_task.task_id,
                "title": saved_task.title,
                "description": saved_task.description,
                "is_complete": bool(saved_task.completed_at)
            }}, 200

    


@tasks_bp.route("", methods=["GET","POST"])
def handle_tasks():

    # Get Tasks: Getting Saved Tasks (Returns 200 OK)
    if request.method == "GET":

        # this code replaces the previous query all code
        sort_query = request.args.get("sort")
        if sort_query == "asc":
            tasks = Task.query.order_by(asc(Task.title))
            
        elif sort_query == "desc": 
            tasks = Task.query.order_by(desc(Task.title))

        else:
            tasks = Task.query.all()
        # end of the new code


        tasks_response = []

        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            })

        return jsonify(tasks_response), 200

    # Create a Task: Valid Task With null completed_at (Returns 201)
    elif request.method == "POST":
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

        return { "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
        }}, 201


    

