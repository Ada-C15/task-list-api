from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
from app import db
from datetime import datetime
from sqlalchemy import asc, desc
from app import slack_app

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():

    request_body = request.get_json()

    if ("title" not in request_body.keys() or
        "description" not in request_body.keys() or
        "completed_at" not in request_body.keys()):
        return {"details": "Invalid data"}, 400

    else:
        new_task = Task(title = request_body["title"],
                        description = request_body["description"],
                        completed_at = request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()

        return {
            "task": new_task.to_json()
            }, 201


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def read_by_title():

    query_string = request.args.get("sort")

    if query_string == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    
    elif query_string == "desc":
        tasks = Task.query.order_by(desc(Task.title))

    else:
        tasks = Task.query.all()
    
    task_response = []

    for task in tasks:
        task_response.append(task.to_json())
    
    return jsonify(task_response), 200


@tasks_bp.route("/<int:task_id>", methods=["GET"], strict_slashes=False)
def read_by_id(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return("", 404)
    
    else:
        return {"task": task.to_json()}, 200


@tasks_bp.route("/<int:task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return("", 404)

    else:
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()

        return {"task": task.to_json()}


@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):

    task = Task.query.get(task_id)

    if task == None:
        return("", 404)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}, 200


@tasks_bp.route("/<int:task_id>/mark_complete", methods=["PATCH"])
def update_completed_task(task_id):

    task = Task.query.get(task_id)

    if task == None:
        return("", 404)
    
    else:
        task.completed_at = datetime.now()
        db.session.commit()
        slack_app.slack_bot_message(task)
        return {"task": task.to_json()}, 200

    
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes = False)
def update_incomplete_task(task_id):

    task = Task.query.get(task_id)

    if task == None:
        return ("", 404)

    else:
        task.completed_at = None
        db.session.commit()

        return {"task": task.to_json()}, 200

#------------------------routes_for_goals----------------------

@goals_bp.route("", methods=["GET"], strict_slashes=False)
def read_by_title():
    query_string = request.args.get("sort")

    if query_string == "asc":
        goals = Goal.query.order_by(asc(Goal.title))
    
    elif query_string == "desc":
        goals = Goal.query.order_by(desc(Goal.title))

    else:
        goals = Goal.query.all()
    
    goal_response = []

    for goal in goals:
        goal_response.append(goal.json_response())
    
    return jsonify(goal_response), 200

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal == None:
        return("", 404)
        
    else: 
        if request.method == "GET":
            return {"goal": goal.json_response()}, 200

        elif request.method == "PUT":
            goals = request.get_json()
            goal.title = goals["title"]
            db.session.commit()
            return {"goal": goal.json_response()}, 200

        elif request.method == "DELETE":
            db.session.delete(goal)
            db.session.commit() 
            goal_response = {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}
            return make_response(goal_response, 200)

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_goals():
    request_body = request.get_json()

    if "title" not in request_body.keys():
        return make_response({"details": "Invalid data"}, 400)

    goal = Goal(title=request_body["title"])

    db.session.add(goal)
    db.session.commit()

    return {
        "goal": goal.json_response()
    }, 201

@goals_bp.route("/<goal_id>/tasks", methods=["GET", "POST"])
def handle_goal_tasks(goal_id):

    goal = Goal.query.get(goal_id)

    if goal == None:
        return ("", 404)
    
    else:
        
        request_body = request.get_json()
        if request.method == "GET":
            task_list = []
            tasks = Task.query.join(Goal).filter('goal_id')
            task_list.append(tasks)

            for task in task_list:
                return {
                    "task": {
                    "id": task.task_id,
                    "goal_id": goal.goal_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": False if task.completed_at is None else True
            }
        }
            # loop through list to turn each result into dictionary
        
        elif request.method == "POST":
            task_list = request_body["task_ids"]

            for id in task_list:
        
                task = Task.query.get(id)
                goal.tasks.append(task)

            db.session.commit()

            return {
                "id": goal.goal_id,
                "task_ids": task_list
            }   

            

    


