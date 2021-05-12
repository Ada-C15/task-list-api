from app import db, SLACK_TOKEN
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def is_complete_helper_function(completed_at):
    if completed_at is None:
        return False
    else:
        return True

@tasks_bp.route("", methods = ["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        sort_query = request.args.get("sort")
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title).all()
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
        else:
            tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False})
        return jsonify(tasks_response)
    elif request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return make_response({
        "details": "Invalid data"
    }, 400)
        else:
            new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=request_body["completed_at"])
            db.session.add(new_task)
            db.session.commit()
            return make_response(
                    { "task": {
                    "id": new_task.task_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": is_complete_helper_function(new_task.completed_at)
                    }}, 201)
            


@tasks_bp.route("/<task_id>", methods = ["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
            return make_response("", 404)
    if request.method == "GET":
        return {"task":{
                    "id": task.task_id,
                    "goal_id": task.goals_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": False    
        }}
    elif request.method == "PUT":
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return make_response(jsonify({"task":{
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": is_complete_helper_function(task.completed_at)}}))
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response(jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"})) 



@tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])  
def mark_complete(task_id): 
    task = Task.query.get(task_id)    
    form_data = request.get_json()
    if task is None:
            return make_response("", 404)
    task.completed_at = datetime.now()
    db.session.commit()
    url = "https://slack.com/api/chat.postMessage"
    key_params = {
                "channel":"task-notifications",
                "text": f"Someone just completed the task {task.title}"
                }
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    requests.post(url, data = key_params, headers = headers)
    return make_response(jsonify({"task":{
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": True}}))
    

@tasks_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])  
def patch_incomplete_on_completed_task(task_id): 
    task = Task.query.get(task_id)    
    form_data = request.get_json()
    if task is None:
            return make_response("", 404)
    if task.completed_at is None:
        db.session.commit()   
        return make_response(jsonify({"task":{
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": False}}))
    else:
        task.completed_at = None
        db.session.commit()   
        return make_response(jsonify({"task":{
                        "id": task.task_id,
                        "title": task.title,
                        "description": task.description,
                        "is_complete": False}}))       

@goals_bp.route("", methods = ["GET", "POST"])
def handle_goals():
    if request.method == "GET":
        goals = Goal.query.all()
        goals_response = []
        for goal in goals:
            goals_response.append({
                "id": goal.goal_id,
                "title": goal.title
                })
        return jsonify(goals_response)
    elif request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return make_response({"details": "Invalid data"}, 400)    
        new_goal = Goal(title=request_body["title"])
        db.session.add(new_goal)
        db.session.commit()
        return make_response({ "goal": {
                        "id": new_goal.goal_id,
                        "title": new_goal.title
                        }}, 201)

@goals_bp.route("/<goal_id>", methods = ["GET", "PUT", "DELETE"])
def handle_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
            return make_response("", 404)
    if request.method == "GET":
        return {"goal":{
                    "id": goal.goal_id,
                    "title": goal.title   
        }}
    elif request.method == "PUT":
        form_data = request.get_json()
        goal.title = form_data["title"]
        db.session.commit()
        return make_response({ "goal": {
                        "id": goal.goal_id,
                        "title":goal.title
                        }})
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return make_response(jsonify({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"})) 

@goals_bp.route("<goal_id>/tasks", methods = ["POST"])
def post_tasks_and_goal(goal_id):
    goal = Goal.query.get(goal_id)
    request_body = request.get_json()
    for each_task in request_body["task_ids"]:
        task = Task.query.get(each_task)
        goal.tasks.append(task)
    db.session.commit()
    task_list = []
    for task in goal.tasks:
        task_list.append(task.task_id)
    return make_response({
            "id": goal.goal_id,
            "task_ids": task_list
            })

@goals_bp.route("<goal_id>/tasks", methods = ["GET"])
def tasks_and_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)
    if len(goal.tasks) == 0:
        return make_response({
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": goal.tasks
        })
    elif len(goal.tasks) > 0:
        list_of_tasks = []
        for each_task in goal.tasks:
            list_of_tasks.append( {
                "id": each_task.task_id,
                "goal_id": goal.goal_id,
                "title": each_task.title,
                "description": each_task.description,
                "is_complete": is_complete_helper_function(each_task.completed_at)
            })
        return make_response({
                    "id": goal.goal_id,
                    "title": goal.title,
                    "tasks": list_of_tasks
            })
        

# @goals_bp.route("<goal_id>/tasks", methods = ["GET"])
# def tasks_and_goal(goal_id):
#     goal = Goal.query.get(goal_id)
#     if goal is None:
#         return make_response("", 404)
#     if len(goal.tasks) == 0:
#         return make_response({
#             "id": goal.goal_id,
#             "title": goal.title,
#             "tasks": goal.tasks
#         })
#     elif len(goal.tasks) > 0:
#         tasks_and_goal_response = []
#         for task in goal.tasks:
#             tasks_and_goal_response.append({
#                     "id": goal.goal_id,
#                     "title": goal.title,
#                     "tasks": 
#             })
#     return jsonify(tasks_and_goal_response)