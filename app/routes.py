from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
import datetime
import requests



tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods = ["GET"])
def task_index():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
        
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    return jsonify(tasks_response), 200


@tasks_bp.route("", methods = ["POST"])
def tasks():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return make_response({ "details": "Invalid data"}, 400)
    else:  
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])
        db.session.add(new_task)
        db.session.commit()
        return make_response(jsonify({"task": new_task.to_json()}), 201)

@tasks_bp.route("/<task_id>", methods = ["GET", "PUT", "DELETE"])
def handle_tasks(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    if request.method == "GET":
        if not task.goal_num:
            return {"task": task.to_json()}, 200
        else:
            return {"task": {
                "id": task.task_id, 
                "goal_id": task.goal_num,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete(),
            }}, 200

    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]

        db.session.commit()

        return { "task": task.to_json()}
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({
            "details":f"Task {task.task_id} \"{task.title}\" successfully deleted"
        }, 200) 

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):

    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    elif not task.is_complete(): 
        task.completed_at = datetime.datetime.now()
        db.session.commit()

    path = "https://slack.com/api/chat.postMessage"

    headers = {'Authorization': 'Bearer SLACK_API_KEY'}

    query_params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}",
        "format": "json"
    }

    response = requests.post(path, params=query_params, headers = headers)
    return {"task": task.to_json()}, 200

    
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    elif task.is_complete(): 
        task.completed_at = None
    return {"task": task.to_json()}, 200



goals_bp = Blueprint("goals", __name__, url_prefix="/goals")



@goals_bp.route("", methods = ["POST"])
def goals():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({ "details": "Invalid data"}, 400)
    else:
        new_goal = Goal(title = request_body["title"])

        db.session.add(new_goal)
        db.session.commit()

        return make_response(jsonify({"goal": new_goal.to_json()}), 201)

@goals_bp.route("", methods = ["GET"])
def goal_index():
    goals = Goal.query.all()
        
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_json())
    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods = ["GET", "PUT", "DELETE"])
def handle_goals(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)
    if request.method == "GET":
        return {"goal": goal.to_json()}, 200
    elif request.method == "PUT":
        get_data = request.get_json()

        goal.title = get_data["title"]
        db.session.commit()
        return {"goal": goal.to_json()}
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return make_response({
                "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
}, 200)

@goals_bp.route("/<goal_id>/tasks", methods = ["POST"])
def goal_tasks(goal_id):
    goal = Goal.query.get(goal_id)
    request_body = request.get_json()
    for elm in request_body["task_ids"]:
        task = Task.query.filter_by(task_id = elm).first()
        if task not in goal.tasks:
            goal.tasks.append(task)
    return {
            "id": goal.goal_id,
            "task_ids": [task.task_id for task in goal.tasks]
        }, 200
    
@goals_bp.route("/<goal_id>/tasks", methods = ["GET"])
def get_tasks(goal_id):
    goal = Goal.query.get(goal_id)
    task = Task.query.filter_by(goal_num=goal_id).first()
    if goal is None:
        return make_response("", 404)
    if task is None:
        return make_response({
                "id": goal.goal_id,
                "title": goal.title,
                "tasks": []
            }, 200)
    elif task in goal.tasks:
        return make_response({
                "id": goal.goal_id,
                "title": goal.title,
                "tasks": [
                    {
                        "id": task.task_id, 
                        "goal_id": task.goal_num,
                        "title": task.title,
                        "description": task.description,
                        "is_complete": task.is_complete(),
                    }
                ]
            }, 200)




    
    
    
        
    




        





    
    

    
















