from app import db 
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify, Flask 
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc 
import os
from dotenv import load_dotenv
import requests

load_dotenv() # parse .env file and load all relevant env vars

# instantiate blueprints of all models
task_bp = Blueprint("tasks", __name__, url_prefix="/tasks") # blueprint class is invoked to allow for app functions to be defined (in routes below) 
goal_bp = Blueprint("goals", __name__, url_prefix="/goals") # without requiring the instance of the object of that bp to exist yet

# TASK ROUTES
@task_bp.route("", methods=["POST"]) # run the .route method on task_bp, have it look for X API call and run the following logic
def create_task():
    """Create a task for the database"""
    request_body = request.get_json() # {'title': 'refresh on topic for SL', 'description': 'run through all routes', 'completed_at': None}

    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_task = Task(title=request_body["title"],
                    description=request_body["description"], 
                    completed_at=request_body["completed_at"])
    
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"task": new_task.to_json()}), 201 # jsonify() ensures proper data serialization: {'task': {'id': 4, 'title': 'test addtl tadfadefsdask', 'description': 'print statement', 'is_complete': False}} 

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    """Get multiple tasks per request"""
    hold_tasks = [] # for hold the collection of dicts later
    tasks_ordered = request.args.get("sort") # request is a Flask obj that has methods .args and .get(); "sort" cue taken from wv 2 tests

    if not tasks_ordered: # if doesnt exist
        tasks = Task.query.all() # pull everything
    elif tasks_ordered == "asc": # otherwise if the str cmd you got was asc (asc cue from tests),
        tasks = Task.query.order_by(asc(Task.title)) # sort in asc order; asc() method's from SQLAlchemy lib
    elif tasks_ordered == "desc": # "" desc
        tasks = Task.query.order_by(desc(Task.title))
    
    if not tasks: # if none exist
        return jsonify(hold_tasks) # return []

    for task in tasks: # otherwise
        hold_tasks.append(task.to_json()) # append properly formatted tasks to list for later return
    return jsonify(hold_tasks) # list of dicts or []

@task_bp.route("/<task_id>", methods=["GET"])
def get_single_task(task_id):
    """ Get single task and its data"""
    single_task = Task.query.get(task_id)

    if not single_task:
        return make_response("", 404)

    associated_goal_id = single_task.goal_id
    dict_single_task = single_task.to_json() 

    if single_task.goal_id:
        dict_single_task["goal_id"] = associated_goal_id
        return jsonify({"task": dict_single_task})
    return jsonify({"task": dict_single_task})

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task_element(task_id):
    """Overwrites a task with details provided by the user"""
    task = Task.query.get(task_id)

    if not task:
        return make_response("", 404)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    #task.completed_at = request_body["completed_at"] # C15 tests look for this, C16's do not

    db.session.commit()
    return jsonify({"task": task.to_json()})

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """ Delete specific task"""
    task = Task.query.get(task_id)

    if not task:
        return make_response("", 404)
    
    db.session.delete(task)
    db.session.commit()
    return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    """Mark a task complete, send confirmation notification"""
    task = Task.query.get(task_id)
    if not task:
        return make_response("", 404)

    task.completed_at = datetime.now()
    db.session.commit()

    target_url = "https://slack.com/api/chat.postMessage"
    LC_SLACK_KEY = os.environ.get("LC_SLACK_KEY")
    headers = {"Authorization": LC_SLACK_KEY}
    data = {
        "channel": "C0220R1781W",
        "text": f"Someone just completed the task {task.title}"}
    requests.patch(target_url, headers=headers, data=data)

    return jsonify({"task": task.to_json()})

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    """Mark a task incomplete"""
    task = Task.query.get(task_id)
    if not task:
        return make_response("", 404)

    task.completed_at = None
    db.session.commit()
    return jsonify({"task": task.to_json()})

# GOAL ROUTES
@goal_bp.route("", methods=["POST"])
def create_goal():
    """Create a goal for the database"""
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_goal = Goal(title=request_body["title"])
    
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({"goal": new_goal.to_json()}), 201

@goal_bp.route("", methods=["GET"])
def get_goals():
    """Get multiple goals per request"""
    hold_goals = []
    goals = Goal.query.all()
    if not goals:
        return jsonify(hold_goals)
    for goal in goals:
        hold_goals.append(goal.to_json())
        return jsonify((hold_goals))

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_single_goal(goal_id):
    """Get single goal and its data"""
    single_goal = Goal.query.get(goal_id)
    if not single_goal:
        return make_response("", 404)
    return jsonify({"goal": single_goal.to_json()})

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    """Overwrite a goal with details supplied by a user"""
    goal = Goal.query.get(goal_id)
    if not goal:
        return make_response("", 404)

    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return jsonify({"goal": goal.to_json()})

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    """Delete a specific goal"""
    goal = Goal.query.get(goal_id)
    if not goal:
        return make_response("", 404)

    db.session.delete(goal)
    db.session.commit()
    return make_response({'details': f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_goal_w_tasks(goal_id):
    """Assigns related tasks to a goal"""

    goal_id = int(goal_id) # incoming str > int
    request_body = request.get_json() # rmr: {'title': 'testadsfasde goal'} >>> key err; {'title': 'testadsfasde goal', 'task_ids': [1, 2]} √
    task_ids = request_body["task_ids"] # list of ints; wrote to appease the tests... in postman, include attr task_ids set to [] or [1,3,2,4]

    for task_id in task_ids: # for every int in the list of ints
        task = Task.query.get(task_id) # build back each int's asso'd task
        task.goal_id = goal_id # ensure that each built-back task has the same goal id
        db.session.add(task)
        db.session.commit()

    return make_response({"id": goal_id, "task_ids": task_ids}, 200) # purely for tests

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_single_tasked_goal(goal_id):
    """Gets a goal and its associated tasks"""

    goal_id = int(goal_id)
    hold_related_tasks = []
    goal = Goal.query.get(goal_id)

    if not goal:
        return make_response("", 404)

    for task in goal.tasks: # for every task id int in the list called tasks on the goal.py side: 
        hold_related_tasks.append(task.to_json()) # append properly formatted task to arbitrary list for final return

    for i in range(len(hold_related_tasks)):
        hold_related_tasks[i]["goal_id"] = goal_id # make sure goal id is correct and the same for each task

    print(goal.goal_id) # 1, √ 
    print(goal.title) # 'test goal', √
    print(hold_related_tasks) # [{'id': 1, 'title': 'refresh on topic for SL', 'description': 'run through all routes', 'is_complete': False, 'goal_id': 1}, 
                                # {'id': 2, 'title': 'test addtl task', 'description': 'print statement', 'is_complete': False, 'goal_id': 1}, 
                                # {'id': 4, 'title': 'test addtl tadfadefsdask', 'description': 'print statement', 'is_complete': False, 'goal_id': 1}] √

    return jsonify({ # whole thing evals to the following when jsonify or make_response are in play: <Response 542 bytes [200 OK]>
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": hold_related_tasks
            })
