
from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify
import datetime


task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["GET", "POST"], strict_slashes=False)

def handle_task():

    if request.method == "GET":

        tasks = Task.query.all()
        tasks_response = []

        if tasks is None:
            return make_response(f"{tasks_response}", 200)

        else:
            for task in tasks:
                tasks_response.append({
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": bool(task.completed_at)
                })

            sort_by_title = request.args.get("sort")

            if sort_by_title: 
                if sort_by_title == "asc": 
                    sorted_asc = sorted(tasks_response, key = lambda i: i["title"])
                    
                    return jsonify(sorted_asc), 200
                elif sort_by_title == "desc":
                    sorted_desc = sorted(tasks_response, key = lambda i:i["title"], reverse = True)

                    return jsonify(sorted_desc), 200
            else:

                return jsonify(tasks_response)

    elif request.method == "POST":

        request_body = request.get_json()

        if all(key in request_body for key in ("title", "description", "completed_at")):
            new_task = Task(title=request_body["title"],
                description=request_body["description"],
                completed_at=request_body["completed_at"])

            db.session.add(new_task)
            db.session.commit()

            tasks_response = {
                    "id": new_task.task_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": bool(new_task.completed_at)
                    }
            dict_copy = tasks_response.copy()
            response = {"task": dict_copy}


            return jsonify(response), 201
        
        else:
            response = {"details": "Invalid data"}
            return jsonify(response), 400
        

    
@task_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])

def get_one_task(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404
        
    elif request.method == "GET":

        tasks_response = {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
                }
        dict_copy = tasks_response.copy()
        response = {"task": dict_copy}

        return jsonify(response)

    elif request.method == "PUT":

        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at=form_data["completed_at"]

        db.session.commit()

        tasks_response = {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
                }

        dict_copy = tasks_response.copy()
        response = {"task": dict_copy}

        return jsonify(response), 200
    
    elif request.method == "DELETE":

        db.session.delete(task)
        db.session.commit()

        text = f"Task {task.task_id} \"{task.title}\" successfully deleted"
        
        response = {"details": text}

        return jsonify(response), 200 

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])

def mark_complete(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    elif request.method == "PATCH":

        task.completed_at = datetime.datetime.now()

        db.session.commit()

        tasks_response = {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
                }

        dict_copy = tasks_response.copy()
        response = {"task": dict_copy}

        return jsonify(response), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])

def mark_incomplete(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    elif request.method == "PATCH":

        task.completed_at = None

        db.session.commit()

        tasks_response = {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
                }

        dict_copy = tasks_response.copy()
        response = {"task": dict_copy}

        return jsonify(response), 200






