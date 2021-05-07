
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
import datetime

goal_bp = task_bp = Blueprint("goal", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["GET", "POST"], strict_slashes=False)

def handle_goal():

    if request.method == "GET":

        goals = Goal.query.all()
        response = []

        if not goals:
            return jsonify(response), 200


        for goal in goals:
            response.append({
                "id": goal.goal_id,
                "title": goal.title
            })
        
        return jsonify(response), 200
    
    elif request.method == "POST":

        request_body = request.get_json()

        if request_body:
            new_goal = Goal(title=request_body["title"])

            db.session.add(new_goal)
            db.session.commit()

            goal_response = {
                    "id": new_goal.goal_id,
                    "title": new_goal.title
                    }
            dict_copy = goal_response.copy()
            response = {"goal": dict_copy}

            return jsonify(response), 201
        
        else: 
            response = {"details": "Invalid data"}
            return jsonify(response), 400


@goal_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])

def get_one_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404

    elif request.method == "GET":

        goal_response = {
                "id": goal.goal_id,
                "title": goal.title,
                }

        dict_copy = goal_response.copy()
        response = {"goal": dict_copy}

        return jsonify(response), 200
    
    elif request.method == "PUT":

        form_data = request.get_json()

        goal.title = form_data["title"]

        db.session.commit()

        goal_response = {
                "id": goal.goal_id,
                "title": goal.title
                }

        dict_copy = goal_response.copy()
        response = {"goal": dict_copy}

        return jsonify(response), 200
    
    elif request.method == "DELETE":

        db.session.delete(goal)
        db.session.commit()

        text = f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        
        response = {"details": text}

        return jsonify(response), 200 
    

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["GET", "POST"], strict_slashes=False)

def handle_task():

    if request.method == "GET":

        sort_by_title = request.args.get("sort")

        if sort_by_title == "asc": 
            # sorted_asc = sorted(tasks_response, key = lambda i: i["title"])
            tasks = Task.query.order_by(Task.title.asc())
            
        elif sort_by_title == "desc":
            # sorted_desc = sorted(tasks_response, key = lambda i:i["title"], reverse = True)
            tasks = Task.query.order_by(Task.title.desc())
                
        else:
            tasks = Task.query.all()

        tasks_response = []

        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            })

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






