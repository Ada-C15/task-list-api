from flask import Blueprint
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import jsonify
from flask import request, make_response
from datetime import datetime 
import os
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


def missing_data():
    return ({"details": "Invalid data"}, 400)


@tasks_bp.route("", methods=["POST"])
def handle_tasks():
    request_body = request.get_json()

    if not "title" in request_body or not request_body.get("title"): 
        return missing_data()
    if not "description" in request_body or not request_body.get("description"):
        return missing_data()
    if "completed_at" not in request_body:
        return missing_data()
    new_task = Task(title=request_body["title"], 
    description=request_body["description"], 
    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()
    return make_response({"task":new_task.to_json()}, 201)


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    title_query_sort = request.args.get("sort")
    if title_query_sort == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()    
    elif title_query_sort == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:        
        tasks = Task.query.all() 
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    return jsonify(tasks_response), 200 


def task_not_found(task_id):
    return make_response("", 404)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return ({"details":f"Task {task_id} \"{task.title}\" successfully deleted"}, 200) 
    return task_not_found(task_id)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return make_response({"task":task.to_json()}, 200)
    return task_not_found(task_id)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        new_data = request.get_json()
        task.title = new_data["title"]
        task.description = new_data["description"]
        task.completed_at = new_data["completed_at"]

        db.session.commit()
        return make_response({"task":task.to_json()}, 200)
    return task_not_found(task_id)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def marking_complete(task_id):
    task = Task.query.get(task_id)
    if task:
        new_data = request.get_json()
        if task.completed_at == None:
            task.completed_at = datetime.today()
            db.session.commit()

            TOKEN = os.environ.get("SLACK_KEY")
            path = "https://slack.com/api/chat.postMessage"
            headers = {"authorization": f"Bearer {TOKEN}"}
            
            query_params = {
                "channel": "task-notifications",
                "text": f"Someone just completed the task {task.title}", 
            }
            response = requests.post(path, query_params, headers=headers)

        return make_response({"task":task.to_json()}, 200)
    return task_not_found(task_id)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"]) 
def marking_incomplete(task_id):
    task = Task.query.get(task_id)
    if task:
        new_data = request.get_json()
        if task.completed_at != None:
            task.completed_at = None 
            db.session.commit()
        return make_response({"task":task.to_json()}, 200)
    return task_not_found(task_id)




@goals_bp.route("", methods=["POST"])
def handle_goals():
    request_body = request.get_json()
    if not "title" in request_body or not request_body.get("title"): 
        return missing_data()
    new_goal = Goal(title=request_body["title"])
    db.session.add(new_goal)
    db.session.commit()
    return make_response({"goal":new_goal.to_json()}, 201)


@goals_bp.route("", methods=["GET"])
def get_goals():        
    goals = Goal.query.all() 
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_json())
    return jsonify(goals_response), 200 


def goal_not_found(goal_id):
    return make_response("", 404)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        return make_response({"goal":goal.to_json()}, 200)
    return goal_not_found(goal_id)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        db.session.delete(goal)
        db.session.commit()
        return ({"details":f"Goal {goal_id} \"{goal.title}\" successfully deleted"}, 200)
    return goal_not_found(goal_id)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        new_data = request.get_json()
        goal.title = new_data["title"]
        db.session.commit()
        return make_response({"goal":goal.to_json()}, 200)
    return goal_not_found(goal_id)




@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def handle_tasked_goals(goal_id):
    tasked_goal = Goal.query.get(goal_id)
    goal_data = request.get_json()
    tasks = [] 
    task_ids = []
    for id in goal_data["task_ids"]:
        task = Task.query.get(id)
        tasks.append(task)
        task_ids.append(int(id))
    tasked_goal.tasks = tasks
    db.session.commit()
    response = {
                "id": int(goal_id),
                "task_ids": task_ids
                }
    return make_response(response, 200) 


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasked_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        goal_data = request.get_json()
        tasks_to_goal = goal.tasks
        tasks_json = []
        for task in goal.tasks:
            tasks_json.append(task.to_json())
        response = {
                    "id": int(goal_id),
                    "title": goal.title,
                    "tasks": tasks_json
        }
        return make_response(response, 200)
    return goal_not_found(goal_id)
