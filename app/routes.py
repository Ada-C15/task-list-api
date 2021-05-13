from werkzeug.datastructures import Authorization
from app import db
from app.models.task import Task
from flask import Blueprint, request, jsonify, make_response
from datetime import datetime
import os
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("/<task_id>", methods=["GET","PUT", "DELETE"])
def get_single_task(task_id):

    task = Task.query.get(task_id)
    # With the GET, POST and DELETE request if there is nothing we output this
    if request == None or task == None:
        return jsonify(None), 404
    # This portion is the GET request for only one task
    elif request.method == "GET":
        return {"task": task.to_json()}, 200
    elif request.method == "PUT":
        # This portion is the PUT request for only one task
        request_body = request.get_json()
        task.title = request_body["title"]
        task.description = request_body["description"]
        # Save action
        db.session.commit()
        return {"task": task.to_json()}, 200
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return {
            "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
            }, 200

@tasks_bp.route("", methods=["GET"])
def tasks_index():
    
    query_sorted = request.args.get("sort")
    if query_sorted == "asc":
        # Found in SQLALchemy documentation. 
        # The order_by method takes the data in the user table (Task) 
        # and filters by title in ascending order
        tasks = Task.query.order_by(Task.title.asc())
    elif query_sorted == "desc":
        # Found in SQLALchemy documentation. 
        # The order_by method takes the data in the user table (Task) 
        # and filters by title in descending order
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    # This portion is the just a GET request
    if tasks == None:
        return []
    else:
        tasks_response = []
        for task in tasks:
            tasks_response.append(task.to_json())
        return jsonify(tasks_response), 200


@tasks_bp.route("", methods=["POST"])
def tasks():
    try:
        # This portion is the POST request
        request_body = request.get_json()
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()

        return {"task": new_task.to_json()}, 201
    except KeyError:
        return {
            "details": "Invalid data"}, 400

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    patch_task = Task.query.get(task_id)
    date = datetime.utcnow()
    if patch_task == None:
        return jsonify(None), 404
    # Mark Complete on an Incompleted Task
    patch_task.completed_at = date
    bot_notification(patch_task)
    db.session.commit()
    
    return {"task":patch_task.to_json()}, 200
    

def bot_notification(patch_task):
    # notification_task = Task.query.get(task_id)
    PATH = "https://slack.com/api/chat.postMessage"
    API_TOKEN = os.environ.get("API_KEY")

    query_params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {patch_task.title}"
    }

    header = {
        "Authorization": f"Bearer {API_TOKEN}"

    }
    result = requests.get(PATH, params=query_params,headers=header)

    return result

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    patch_task = Task.query.get(task_id)
    if patch_task == None:
        return jsonify(None), 404
    patch_task.completed_at = None
    db.session.commit()

    return {"task":patch_task.to_json()}, 200


# ============================Goals=========================================

from app.models.goal import Goal
from flask import Blueprint, request, jsonify

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("",methods=["POST"])
def create_goal():
    try:
        # This portion is the POST request
        request_body = request.get_json()
        new_goal = Goal(title=request_body["title"])

        db.session.add(new_goal)
        db.session.commit()
        return {"goal": new_goal.to_json_goal()}, 201
    except KeyError:
        return {
            "details": "Invalid data"}, 400
@goals_bp.route("", methods=["GET"])
def goals_index():
    # This portion is the just a GET request
    goals = Goal.query.all()
    if goals == None:
        return []
    else:
        goals_response = []
        for goal in goals:
            goals_response.append(goal.to_json_goal())
        return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET","PUT", "DELETE"])
def get_single_goal(goal_id):

    goal = Goal.query.get(goal_id)
    # With the GET, POST and DELETE request if there is nothing we output this
    if request == None or goal == None:
        return jsonify(None), 404
    # This portion is the GET request for only one task
    elif request.method == "GET":
        return {"goal": goal.to_json_goal()}, 200
    elif request.method == "PUT":
        # This portion is the PUT request for only one task
        request_body = request.get_json()
        goal.title = request_body["title"]
        # Save action
        db.session.commit()
        return {"goal": goal.to_json_goal()}, 200
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return {
            "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
            }, 200


# # ===============Establishing One to Many Realtionship=================================


@goals_bp.route("<goal_id>/tasks", methods=["POST"])
def post_tasks_ids_to_goal(goal_id):
    goal = Goal.query.get(goal_id)
    request_body = request.get_json()
    # Post

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        goal.tasks.append(task)
    db.session.commit()
    return make_response({"id": goal.goal_id, "task_ids": request_body["task_ids"]}, 200)

@goals_bp.route("<goal_id>/tasks", methods=["GET"])
def getting_tasks_of_one_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal == None:
        return jsonify(None), 404
    else:
        tasks_from_goal = goal.tasks

        tasks_response = []
        for task in tasks_from_goal:
            tasks_response.append(task.to_json())

        return {"id":goal.goal_id,"title": goal.title, "tasks": tasks_response}, 200