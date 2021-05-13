from flask import Blueprint, request, make_response, jsonify
from sqlalchemy import asc, desc
from app import db 
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import requests
import os


tasks_bp = Blueprint(
    "tasks",
    __name__, 
    url_prefix="/tasks"
)

# create a new task 
@tasks_bp.route("", methods=["POST"])
def add_new_task():
    request_body = request.get_json()
    try:
        request_body["title"] 
        request_body["description"] 
        request_body["completed_at"] 
    except: 
        return make_response(jsonify({
        "details": "Invalid data"
        }),400)

    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_json()}, 201)

# get all tasks asc, desc, unsorted
@tasks_bp.route("", methods=["GET"])
def list_all_tasks(): 
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(asc("title"))
    elif sort_query == "desc": 
        tasks = Task.query.order_by(desc("title"))
    else: 
        tasks = Task.query.all()
        # matt asked in order to google 
        # find out what type of data tasks is so i can look at methods for that in documentation 
    tasks_response = []
    for task in tasks: 
        tasks_response.append(task.to_json())
    return jsonify(tasks_response)

# get one task by id 
@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = Task.query.get(task_id)
    if task: 
        task_response = {"task": task.to_json()}
        return task_response 
    
    return make_response("Task not found. Less to do then :)", 404)

# update one task by id 
@tasks_bp.route("/<int:task_id>", methods=["PUT"])
def update_task_by_id(task_id): 
    task = Task.query.get(task_id)
    if task: 
        request_body = request.get_json()

        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body["completed_at"]

        db.session.commit()

        return make_response({"task": task.to_json()})

    return make_response("", 404)

# mark compelte on an incompleted task
@tasks_bp.route("/<int:task_id>/<complete_status>", methods=["PATCH"])
# status is a route paramter
# how to know if it a query param
def patch_task_by_id(task_id, complete_status): 
    task = Task.query.get(task_id)
    # PATH = "https://slack.com/api/chat.postMessage"

    # status = request.args.get("complete_status")
    # dont need bc complete_status is a route parameter 
    if task is None: 
        return make_response("", 404)
        # refactor option: make a 404 message 

    if complete_status == "mark_complete": 
        date = datetime.today()
        task.completed_at = date
        send_slack_notification(task)
        # query_params = {
        #     "channel": "task-notifications",
        #     "text": "u done did it"
        # }
        
        # headers = {
        #     "Authorization" : f"Bearer {os.getenv('SLACK_TOKEN')}"
        # }
        # response = requests.post(PATH, params=query_params, headers=headers)

    else:
        task.completed_at = None

    db.session.commit()

    return make_response({"task": task.to_json()})

def send_slack_notification(task): #add parameter for which task it is

    PATH = "https://slack.com/api/chat.postMessage"
    query_params = {
        "channel": "task-notifications",
        "text": "u done did it"
    }
    
    headers = {
        "Authorization" : f"Bearer {os.getenv('SLACK_TOKEN')}"
    }
    requests.post(PATH, params=query_params, headers=headers)


# delete one task by id 
@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task_by_id(task_id):
    task = Task.query.get(task_id)
    if task: 
        db.session.delete(task)
        db.session.commit()
        return make_response({
        "details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'
    })
    
    return make_response("", 404)

'''
goal routes
'''
goals_bp = Blueprint(
    "goals",
    __name__, 
    url_prefix="/goals"
)

# create a new goal 
@goals_bp.route("", methods=["POST"])
def add_new_goal():
    request_body = request.get_json()
    try:
        request_body["title"] 
    except: 
        return make_response(jsonify({
        "details": "Invalid data"
        }),400)

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_json()}, 201)

# get all goals asc, desc, unsorted
@goals_bp.route("", methods=["GET"])
def list_all_goals(): 
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        goals = Goal.query.order_by(asc("title"))
    elif sort_query == "desc": 
        goals = Goal.query.order_by(desc("title"))
    else: 
        goals = Goal.query.all()
        # matt asked in order to google 
        # find out what type of data goals is so i can look at methods for that in documentation 
    goals_response = []
    for goal in goals: 
        goals_response.append(goal.to_json())
    return jsonify(goals_response)

# get one goal by id 
@goals_bp.route("/<int:goal_id>", methods=["GET"])
def get_task_by_id(goal_id):
    goal = Goal.query.get(goal_id)
    if goal: 
        goal_response = {"goal": goal.to_json()}
        return goal_response 
    
    return make_response("Goal not found. Less to do then :)", 404)

# update one goal by id 
@goals_bp.route("/<int:goal_id>", methods=["PUT"])
def update_goal_by_id(goal_id): 
    goal = Goal.query.get(goal_id)
    if goal: 
        request_body = request.get_json()

        goal.title = request_body["title"]

        db.session.commit()

        return make_response({"goal": goal.to_json()})

    return make_response("", 404)

# delete one goal by id 
@goals_bp.route("/<int:goal_id>", methods=["DELETE"])
def delete_goal_by_id(goal_id):
    goal = Goal.query.get(goal_id)
    if goal: 
        db.session.delete(goal)
        db.session.commit()
        return make_response({
        "details": 'Goal 1 "Build a habit of going outside daily" successfully deleted'
    }, 200)
    
    return make_response("", 404)

# NESTED  inside of goals 

# post a list of task IDs to a goal 
@goals_bp.route("/<int:goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = Goal.query.get(goal_id)
    request_body = request.get_json() # this is a dictionary

    if goal is None: 
        return make_response("", 404)
    
    # updated_goal = Goal(title=request_body["title"])
    
    # iterate thru each task id 
    for task_id in request_body["task_ids"]:
        # call each task by id (element)
        task = Task.query.get(task_id)
        # update the backref value to goal_id 
        task.goal_id = goal_id

    db.session.commit()

    return make_response(jsonify(id=goal_id, task_ids=request_body["task_ids"]), 200)

# see all messages for a specific user 
@goals_bp.route("/<int:goal_id>/tasks", methods=["GET"])
def get_all_tasks_in_one_goal(goal_id): 
    # find a goal 
    goal = Goal.query.get(goal_id)

    if goal is None: 
        return make_response("", 404)
    
    goal_response = goal.to_json()
    # add new key to dictionary of goal response
    goal_response["tasks"] = []
    # goal_response["tasks"] = goal.tasks 
    # iterate thru the tasks in the fake column in goal.tasks
    # print(goal.tasks)
    # tasks = goal.tasks
    for task in goal.tasks: 
        # add each task record in goal.tasks to list 
        goal_response["tasks"].append(task.to_json())
    
    return jsonify(goal_response)


