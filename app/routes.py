from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import datetime
from sqlalchemy import DateTime, desc
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#wave6
@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes= False)
def task_goal(goal_id):
    request_body = request.get_json()
    goal = Goal.query.get(goal_id)

    if goal is None:
        return make_response("", 404)

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        task.goal_id = goal.goal_id
 
    db.session.commit()   
    return make_response({"id": goal.goal_id, "task_ids": request_body["task_ids"]}, 200)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes= False)
def get_goal_task(goal_id):
    goal = Goal.query.get(goal_id)
    if goal == None:
        return make_response("", 404)
    
    tasks = Task.query.filter_by(goal_id = goal_id)
    task_list = []

    for task in tasks:
        task_list.append(helper_fun(task))
    
    return make_response({"id": int(goal_id), "title": goal.title, "tasks": task_list }, 200)

def helper_fun(task_goal):
    return {
            "id": task_goal.task_id,
            "goal_id": task_goal.goal_id,
            "title": task_goal.title,
            "description": task_goal.description,
            "is_complete": task_goal.completed_at != None
        }

#wave 5
@goals_bp.route("", methods=["POST"], strict_slashes= False)
def create_goals():
    request_body = request.get_json()
    
    if "title" in request_body:
        new_goal = Goal(title = request_body["title"])
        db.session.add(new_goal)
        db.session.commit()
        return jsonify({"goal": new_goal.now_json()}), 201
    else:
        return jsonify({"details": "Invalid data"}), 400 

@goals_bp.route("", methods=["GET"], strict_slashes= False)
def get_goals():
    goals = Goal.query.order_by(Goal.title).all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.now_json()) 
    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"], strict_slashes= False)
def get_goal_by_id(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return jsonify(None), 404
    else:
        return make_response({"goal": goal.now_json()}, 200)

@goals_bp.route("/<goal_id>", methods=["PUT"], strict_slashes= False)
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return jsonify(None), 404
    
    form_data = request.get_json()

    goal.title = form_data["title"]
    
    db.session.commit()
    
    return jsonify({"goal":goal.now_json()}), 200 

@goals_bp.route("/<goal_id>", methods=["DELETE"], strict_slashes= False)
def abandon_goals(goal_id):
    goal = Goal.query.get(goal_id) 
    if goal is None:
        return jsonify(None), 404
    else:
        db.session.delete(goal)
        db.session.commit()
    return jsonify({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}), 200
#end wave 5

@tasks_bp.route("", methods=["GET", "POST"], strict_slashes= False)
def deal_tasks():
    if request.method == "GET":
        sort_query = request.args.get("sort")#<- handles second wave 2
        if sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
        else:
            tasks = Task.query.order_by(Task.title).all() #<- handles first wave 2
        tasks_response = []
        for task in tasks:
            tasks_response.append(task.to_json())
        return jsonify(tasks_response)

    elif request.method == "POST":
        request_body = request.get_json()
       
        if "title" in request_body and "description" in request_body and "completed_at" in request_body:
            new_task = Task(title = request_body["title"],
                        description = request_body["description"],
                        completed_at = request_body["completed_at"])
                        
            db.session.add(new_task)
            db.session.commit()
            return make_response({"task": new_task.to_json()}, 201)
        else:
            return jsonify({"details": "Invalid data"}), 400

#also handles wave 6 last test
@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes= False)
def get_task_by_id(task_id):
    task = Task.query.get(task_id)
    goal_attached = task.goal_id
    if task is None:
        return jsonify(None), 404
    elif goal_attached:
        return make_response({"task": helper_fun(task)}, 200)
    else:
        return make_response({"task": task.to_json()}, 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes= False)
def delete_task(task_id):
    print("in delete task") #what is this left over from, testing maybe? get rid of this you silly 
    task = Task.query.get(task_id) 
    if task is None:
        return jsonify(None), 404
    else:
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)


@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes= False)
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify(None), 404
    
    form_data = request.get_json()

    task.title = form_data["title"]
    task.description = form_data["description"]
    task.completed_at = form_data["completed_at"]
    
    db.session.commit()
    
    return jsonify({"task":task.to_json()}), 200

#wave 3
@tasks_bp.route("/<task_id>/mark_complete", methods=["Patch"])
def mark_complete(task_id):
    task= Task.query.get(task_id)
    if not task:
        return "", 404

    if task.completed_at:
        task.completed_at = datetime.datetime.now()
    else:
        task.completed_at = datetime.datetime.now()

    db.session.add(task)
    db.session.commit()

    if task.completed_at:
        return jsonify({
        "task": task.to_json()
        }), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["Patch"])
def mark_incomplete(task_id):
    task= Task.query.get(task_id)
    if not task:
        return "", 404

    if task.completed_at:
        task.completed_at = None
        return {
            "task": task.to_json()
            }, 200
    else:
        task.completed_at = None
        return {
            "task": task.to_json()
            }, 200

  






