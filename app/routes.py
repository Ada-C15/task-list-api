from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
from sqlalchemy import asc, desc
from datetime import datetime
import os
import requests


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
index_bp = Blueprint("index", __name__, url_prefix="/")

@index_bp.route("", methods=["GET"])
def index():
    return make_response("Hello, this is Ruthie's task list", 200)

@index_bp.route("smile/<count>", methods=["GET"])
def smiley(count):
    count_list = []
    for i in range(int(count)):
        count_list.append(";)")
    return make_response(jsonify(count_list), 200)


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_tasks():

    sort_query = request.args.get("sort")
    tasks_response = []
    sorted_response = []
    ordered_query = []

    
    if sort_query is None:
        tasks = Task.query.all()
    
        for task in tasks:           
            tasks_response.append(task.create_json())
            
        return make_response(jsonify(tasks_response), 200)  

    
    if sort_query == "asc":

        ordered_query = Task.query.order_by(Task.title.asc())
        
    elif sort_query == "desc":

        ordered_query = Task.query.order_by(Task.title.desc())
    
    for task in ordered_query:
        sorted_response.append(task.create_json())
    
    return jsonify(sorted_response), 200
        
        
@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_new_task():

    request_body = request.get_json()
    if not request_body or not request_body.get("title") or not request_body.get("description") or "completed_at" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"]
    )
    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.create_json()}, 201)


@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_task_by_id(task_id):
    request_body = request.get_json()
    task = Task.query.get(task_id)

    if task is None:
            return make_response("", 404)

    if task.goal_id is None:
        return make_response({"task": task.create_json()}, 200)
    
    else:
    
        return make_response({"task": task.create_json_with_goal_id()}, 200)      

@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
            return make_response("", 404)

    else:
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()
        return make_response({"task": task.create_json()}, 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):   
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    else:
        db.session.delete(task)
        db.session.commit()

    return make_response({"details":f"Task {task.id} \"{task.title}\" successfully deleted"}, 200)

@tasks_bp.route("<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):
    task = Task.query.get(task_id)

    if task is None:
            return make_response("", 404)

    task.completed_at = datetime.utcnow()
    db.session.commit()

    slack_token = os.environ["SLACK_API_TOKEN"]
    slack_channel = "task-notifications"
    slack_icon_url = "https://slack.com/api/chat.postMessage"
    text = f"Someone just completed the task {task.title}"

    response = requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack_token,
        'channel': slack_channel,
        'text': text,
        'icon_url': slack_icon_url
    }).json()	

    return make_response({"task": task.create_json()}, 200)
    

@tasks_bp.route("<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete(task_id):
    task = Task.query.get(task_id)

    if task is None:
            return make_response("", 404)

    task.completed_at = None
    db.session.commit()

    return make_response({"task": task.create_json()}, 200)


@goals_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_goals():

    goals_response = []
    goals = Goal.query.all()
    
    for goal in goals:           
        goals_response.append(goal.create_goal_json())
        
    return make_response(jsonify(goals_response), 200) 


@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_goals():
    request_body = request.get_json()
    if not request_body or not request_body.get("title"):
        return make_response({"details": "Invalid data"}, 400)

    new_goal = Goal(
        title = request_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.create_goal_json()}, 201)


@goals_bp.route("<goal_id>", methods=["GET"], strict_slashes=False)
def get_one_goal(goal_id):

    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)
    

    return make_response({"goal": goal.create_goal_json()}, 200)


@goals_bp.route("<goal_id>", methods=["PUT"], strict_slashes=False)
def update_goal(goal_id):

    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)
    
    form_data = request.get_json()
    goal.title = form_data["title"]

    db.session.commit()
    return make_response({"goal": goal.create_goal_json()}, 200)


@goals_bp.route("<goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_goal(goal_id):

    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)
    
    else:

        db.session.delete(goal)
        db.session.commit()

    return make_response({"details": f'Goal {goal.id} \"{goal.title}\" successfully deleted'}, 200)


@goals_bp.route("<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def add_tasks_to_goals(goal_id):

    goal_id = int(goal_id)
    request_body = request.get_json()
    task_ids = request_body["task_ids"]
    goal = Goal.query.get(goal_id)

    task_id_list =[]

    if not request_body:
        return make_response({"details": "Invalid data"}, 400)


    for task_id in task_ids:
        task = Task.query.get(task_id)
        task.goal_id = goal_id 

        task_id_list.append(task_id)

        db.session.add(task)
        db.session.commit()  


    return make_response({"id": goal_id, "task_ids": task_id_list}, 200)

@goals_bp.route("<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_tasks_of_one_goal(goal_id):

    goal_id = int(goal_id)
    goal = Goal.query.get(goal_id)


    if not goal:
        return make_response("", 404)
    
    tasks = goal.tasks


    task_list = []
    for task in tasks:

        task_list.append(task.create_json_with_goal_id())

    response = {
        "id" : goal_id,
        "title" : goal.title,
        "tasks" : task_list
    }

    return make_response(response, 200)






