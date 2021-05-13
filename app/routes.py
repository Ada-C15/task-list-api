from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify
from datetime import datetime
import requests
import flask_migrate
import os
from app.models.goal import Goal



task_bp = Blueprint("task", __name__, url_prefix='/tasks')
goal_bp = Blueprint("goal", __name__, url_prefix='/goals')

@task_bp.route("", methods=["POST"], strict_slashes = False)
def post_task():
    request_body = request.get_json()

    if "title" in request_body and "description" in request_body and "completed_at" in request_body:
        new_task = Task(title=request_body["title"],description=request_body["description"], 
                    completed_at=request_body["completed_at"])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"task": new_task.to_json()}), 201
    else: 
        return make_response({"details": "Invalid data"}), 400     
        
    
@task_bp.route("", methods=["GET"], strict_slashes = False)
def get_all_tasks():
    sort_method = request.args.get("sort")
    if sort_method == "asc":
        tasks = Task.query.order_by(Task.title.asc())            
    elif sort_method == "desc":
        tasks = Task.query.order_by(Task.title.desc())   
    else:
        tasks = Task.query.all()
    task_response_body = []  
    for task in tasks:
        task_response_body.append(task.to_json())
    return jsonify(task_response_body), 200

@task_bp.route('/<task_id>', methods=['GET'], strict_slashes = False)
def get_single_task(task_id):  # same name as parameter route
    task = Task.query.get(task_id)
    if not task:
        return "", 404
    return make_response({"task": task.to_json()}), 200    
   
    
@task_bp.route("/<task_id>", methods=['DELETE', 'PUT'], strict_slashes = False)
def delete_or_put_tasks(task_id):
    task = Task.query.get(task_id)
    if not task:
        return "", 404
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({
            "details": f'Task {task_id} "{task.title}" successfully deleted'
            }), 200
        
    elif request.method == 'PUT':
        request_body = request.get_json()   
        task.title = request_body["title"]
        task.completed_at = request_body["completed_at"]
        task.description = request_body["description"]
        db.session.commit()
        return jsonify({"task": task.to_json()}), 200
        
   
@task_bp.route('/<task_id>/mark_complete', methods=["PATCH"], strict_slashes = False) 
def mark_complete(task_id):
    task = Task.query.get(task_id)
    if task == None:
        return make_response(), 404
    
    if task:
        task.completed_at = datetime.utcnow()   
        db.session.commit()  
        call_slack(task)
        return make_response({"task": task.to_json()}, 200)



def call_slack(task):
    key = os.environ.get("API_KEY")
    url = "https://slack.com/api/chat.postMessage"
    slack_str = f"Someone just completed the task {task.title}"
    requests.post(url, data={"token":key ,"channel":"general" , "text": slack_str})



@task_bp.route('/<task_id>/mark_incomplete', methods=["PATCH"], strict_slashes = False)
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task == None:
        return make_response(), 404
   
    task.completed_at = None
    db.session.commit()
    return jsonify({"task": task.to_json()}), 200



@goal_bp.route("", methods=["POST"], strict_slashes = False)
def post_new_goal():
    request_body = request.get_json()

    if "title" in request_body:
        new_goal = Goal(title=request_body["title"])
        db.session.add(new_goal)
        db.session.commit()
        return jsonify({"goal": new_goal.now_json()}), 201
    else: 
        return make_response({"details": "Invalid data"}), 400

@goal_bp.route("", methods=["GET"], strict_slashes = False)
def get_all_goals():
    sort_method = request.args.get("sort")
    if sort_method == "asc":
        goals = Goal.query.order_by(Goal.title.asc())            
    elif sort_method == "desc":
        goals = Goal.query.order_by(Goal.title.desc())   
    else:
        goals = Goal.query.all()
    goal_response_body = []  
    for goal in goals:
        goal_response_body.append(goal.now_json())
    return jsonify(goal_response_body), 200



@goal_bp.route('/<goal_id>', methods=['GET'], strict_slashes = False)
def get_single_goal(goal_id):  
    goal = Goal.query.get(goal_id)
    if not goal:
        return "", 404
    return make_response({"goal": goal.now_json()}), 200
    
@goal_bp.route("/<goal_id>", methods=['DELETE', 'PUT'], strict_slashes = False)
def delete_or_put_goals(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return "", 404
    elif request.method == 'DELETE':
        db.session.delete(goal)
        db.session.commit()
        return jsonify({
            "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
            }), 200
        
    elif request.method == 'PUT':
        request_body = request.get_json()   
        goal.title = request_body["title"]
        db.session.commit()
        return jsonify({"goal": goal.now_json()}), 200


@goal_bp.route("/<int:goal_id>/tasks", methods=["POST"], strict_slashes = False)
def post_new_task(goal_id):
    request_body = request.get_json()
    task_ids = request_body["task_ids"]
    goal = Goal.query.get(goal_id)
    for task_id in task_ids:
        task = Task.query.get(task_id)
        if task.goal_id != goal_id:
            goal.tasks.append(task)
    response_body = {
        "id": goal_id,
        "task_ids": task_ids
    }
    return jsonify(response_body), 200


@goal_bp.route('/<int:goal_id>/tasks', methods=['GET'])
def get_tasks_goals(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return '', 404
    return jsonify(goal.full_json()), 200

    
   




