from app import db 
from flask import Blueprint, request, make_response, jsonify
from app.models.task import Task 
from app.models.goal import Goal
from datetime import datetime
import os 
import requests



task_list_bp = Blueprint("Task",__name__)

@task_list_bp.route("/tasks", methods=["POST"])
def create_a_task(): 
    request_body = request.get_json()

    if not ("title" in request_body
            and "description" in request_body
            and "completed_at" in request_body):
    
       
         return make_response(jsonify({
            "details": "Invalid data"
        }), 400)
        

    new_task = Task(title=request_body["title"],
                description=request_body["description"],
                completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

  

    response = {
            "task": {
                "id": new_task.id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": new_task.is_complete() 
            }
        }
    return make_response(jsonify(response), 201)

@task_list_bp.route("/tasks", methods=["GET"])
def retrieve_all_tasks(): 

    if "sort" in request.args:
        if request.args["sort"] == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
        else:
            tasks = Task.query.order_by(Task.title.asc()).all()
    else:
        tasks = Task.query.all()
    


    return jsonify([
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete() 
        } for task in tasks
    ])

@task_list_bp.route("/tasks/<task_id>", methods=["GET", "PUT", "DELETE"])
def retrieve_one_task(task_id): 
    task = Task.query.filter_by(id = task_id).first()

    if task is None: 
        return make_response("", 404)

    if request.method == "GET": 
        return jsonify({
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete()
            }
        })
    elif request.method == "PUT": 
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]


        db.session.commit()
        
        return jsonify({
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete()
            }
        })

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify (
        {
            "details": (f'Task {task.id} "{task.title}" successfully deleted')
        })
                

@task_list_bp.route("/tasks/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id): 
    task = Task.query.filter_by(id = task_id).first()
    if task is None: 
        return make_response("", 404)

    access_token = os.environ.get("SLACK_BOT_TOKEN")
    path = "https://slack.com/api/chat.postMessage"
    response = requests.post(path, data = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}",
    }, headers = {
        "Authorization": access_token,
    })
    

    if task.is_complete(): 
        task.completed_at = datetime.now() 
        db.session.commit()
        return jsonify({
            "task": {
                "id": task.id, 
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete() 
            }
        })
    else: 
        task.completed_at = datetime.now()
        db.session.commit() 
        return jsonify({
            "task": {
                "id": task.id, 
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete() 
            }
        })
        

@task_list_bp.route("/tasks/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id): 
    task = Task.query.filter_by(id = task_id).first()

    if task is None: 
        return make_response("", 404)


    if task.is_complete(): 
        task.completed_at = None
        db.session.commit()

    return jsonify({
        "task": {
            "id": task.id, 
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete()
        }
    })
    

    

#Routes for Goals

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
@goals_bp.route("", methods=["POST"])
def create_a_goal(): 
    request_body = request.get_json()

    if not ("title" in request_body):        
         return make_response(jsonify({
            "details": "Invalid data"
        }), 400)
        

    new_goal = Goal(title=request_body["title"])
        
    db.session.add(new_goal)
    db.session.commit()


    response = {
            "goal": {
                "id": new_goal.goal_id,
                "title": new_goal.title
        
            }
        }
    return make_response(jsonify(response), 201)

@goals_bp.route("", methods=["GET"])
def retrieve_all_goals():
    goals = Goal.query.all()

    return jsonify([
        {
           "id": goal.goal_id,
           "title": goal.title,
        } for goal in goals
    ])




@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def retrieve_one_goals_tasks(goal_id): 
    goal = Goal.query.filter_by(goal_id=goal_id).first()

    if goal is None: 
        return make_response("", 404)
    
    if request.method == "GET":
       return jsonify(
            {"goal": {
            "id": goal.goal_id,
            "title": goal.title,
            } }
        )

    elif request.method == "PUT": 
        form_data = request.get_json()

        goal.title = form_data["title"]
    
        db.session.commit()
        
        return jsonify({
            "goal": {
                "id": goal.goal_id,
                "title": goal.title,
            }
        })

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return jsonify (
        {
            "details": (f'Goal {goal.goal_id} "{goal.title}" successfully deleted')
        })


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def send_task_ids_goal(goal_id): 
  

    request_body = request.get_json()
    task_ids = request_body['task_ids']
    for task_id in task_ids:
        task = Task.query.filter_by(id = task_id).first()
        task.goal_id = goal_id

    db.session.commit()
    response = {
                "id": int(goal_id),
                "task_ids": task_ids,
            }
    return make_response(jsonify(response), 200)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def retrieve_one_task(goal_id): 
    goal = Goal.query.filter_by(goal_id=goal_id).first()
    tasks = Task.query.filter_by(goal_id = goal_id).all()
    if goal is None: 
        return make_response("", 404)


    response = {
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": [
                {
                "id": task.id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete()
                }
                for task in tasks 
            ]
        }

    return make_response(jsonify(response), 200)