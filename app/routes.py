from flask.wrappers import Response
from app import db
from app.models.task import Task, to_dict
from app.models.goal import Goal, to_json
from flask import Blueprint, request, make_response, jsonify
from datetime import datetime
from dotenv import load_dotenv
import os
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
load_dotenv()

# tasks

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():

    request_body = request.get_json()

    response = {"details": "Invalid data"}

    if "title" not in request_body.keys() or "description" not in request_body.keys() or "completed_at" not in request_body.keys():

        return jsonify(response), 400

    else:
        new_task = Task(title = request_body["title"], description = request_body["description"], completed_at = request_body["completed_at"])
        db.session.add(new_task)
        db.session.commit()
        valid_task = {"task": to_dict(new_task)}

        return jsonify(valid_task), 201


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():

    tasks_response = []

    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())

    else:
        tasks = Task.query.all()

    for task in tasks:
        tasks_response.append(to_dict(task))

    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_task(task_id):

    task = Task.query.get(task_id)

    if request.method == "GET":
        if task is None:
            return make_response(f"404 Not Found", 404) 

        else:
            one_task = to_dict(task)

            return {"task": one_task}


    elif request.method == "PUT":
        if task: 
            form_data = request.get_json()
            task.title = form_data["title"]
            task.description = form_data["description"]
            task.is_complete = form_data["completed_at"]
            db.session.commit()

            updated_task = {
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": bool(task.completed_at)
            }
        else: 
            return make_response(f"", 404) 
           
        return {'task': updated_task}

    elif request.method == "DELETE":
        if task:
            db.session.delete(task)
            db.session.commit()

            response = {"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}

            return jsonify(response), 200
        
        else:
            return make_response(f"", 404)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    task.completed_at = datetime.utcnow()
    db.session.commit()

    slack_bot_notification("Did this work")

    return jsonify({"task": to_dict(task)}), 200

def slack_bot_notification(message):
    path = "https://slack.com/api/chat.postMessage"
    SLACK_KEY = os.environ.get("SLACK_TOKEN")
    headers = {"Authorization": f"Bearer {SLACK_KEY}"}
    query_params = {"channel": "task-notifications", "text": message}
    requests.post(path, params=query_params, headers=headers)


@tasks_bp.route("<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    task.completed_at = None 
    db.session.commit()

    return jsonify({"task": to_dict(task)}), 200
 

# goals

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_goal():
    request_body = request.get_json()

    response = {"details": "Invalid data"}

    if "title" not in request_body.keys():

        return jsonify(response), 400

    else:
        new_goal = Goal(title = request_body["title"])
        db.session.add(new_goal)
        db.session.commit()
        valid_goal = {"goal": to_json(new_goal)}

        return jsonify(valid_goal), 201

@goals_bp.route("", methods=["GET"], strict_slashes=False)
def get_goals():

    goals = Goal.query.all()
    goals_response = []

    if goals != None:

        for goal in goals:
            goals_response.append(to_json(goal))

        return jsonify(goals_response), 200

    return jsonify(goals_response), 200


@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_goal(goal_id):
    
    goal = Goal.query.get(goal_id)

    if request.method == "GET":
        if goal is None:
            return make_response(f"", 404) 
    
        else:
            valid_goal = {"goal": to_json(goal)}
            
            return jsonify(valid_goal), 200

    elif request.method == "PUT":
        if goal: 
            form_data = request.get_json()
            goal.title = form_data["title"]
            db.session.commit()

            updated_goal = {
                    "id": goal.goal_id,
                    "title": goal.title
            }
            
        else: 
            return make_response(f"", 404) 
           
        return {'goal': updated_goal}

    elif request.method == "DELETE":
        if goal:
            db.session.delete(goal)
            db.session.commit()

            response = {"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}

            return jsonify(response), 200
        
        else:
            return make_response(f"", 404)


@goals_bp.route("/<goal_id>/tasks", methods=["POST", "GET"], strict_slashes=False)
def goal_task_relationship(goal_id):
    
    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)

    if request.method == "POST":
        
        response_body = request.get_json()
        task_ids_list = []


        for task_id in response_body["task_ids"]:
            task = Task.query.get(task_id)

            task_ids_list.append(task)

            task.goal_id = goal_id

        db.session.commit()

        return ({"id": int(goal_id), "task_ids": task_ids_list})

    # elif request.method == "GET":

    #     task_goal = []

    #     for task in goal.tasks:
    #         task_goal.append(to_dict(task))

    #     return make_response(jsonify(id=int(goal_id)))
