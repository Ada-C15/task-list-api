from flask import Blueprint
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
import datetime
import os 
import requests 


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks") 
goals_bp = Blueprint("goals", __name__, url_prefix="/goals") 

#### Tasks ###3

@tasks_bp.route("", methods=["POST","GET"])
def handle_tasks():
    if request.method == "POST":
        request_body = request.get_json()
        if 'title' in request_body and 'description' in request_body and 'completed_at' in request_body: 
            new_task = Task(title=request_body["title"],
                            description=request_body["description"],
                            completed_at = request_body["completed_at"])
            db.session.add(new_task)
            db.session.commit()

            return jsonify(new_task.task_response()), 201
        else:
            return make_response ({"details": "Invalid data"},400)

    elif request.method == "GET":
        sort_by_title = request.args.get("sort")
        if sort_by_title == "asc": 
            tasks = Task.query.order_by(Task.title.asc())
        elif sort_by_title == "desc":
            tasks = Task.query.order_by(Task.title.desc())

        else:
            tasks = Task.query.all()
    
        tasks_response = []
        for task in tasks:
            tasks_response.append(task.task_response_lean())
        return jsonify(tasks_response),200

@tasks_bp.route("/<task_id>", methods=["GET","PUT","DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    elif request.method == "GET":
        return jsonify(task.task_response()),200

    elif request.method == "PUT":      
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]

        db.session.commit()
        return jsonify(task.task_response()), 200
        
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        delete_text = f"Task {task.task_id} \"{task.title}\" successfully deleted"
        response = {"details":delete_text}
        return jsonify(response), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    
    task.completed_at = datetime.datetime.now()
    db.session.commit()
    slack_message(task)
    
    return jsonify(task.task_response()), 200

def slack_message(task):
    path = "https://slack.com/api/chat.postMessage"
    query_params = {
        "channel" : "task-notifications",
        "text" : f"Task {task.task_id} with title {task.title} has been marked as complete"
    }
    authorization = os.environ.get('SLACK_TOKEN')
    headers = {"Authorization": f"Bearer {authorization}"}

    response = requests.post(path, data=query_params, headers=headers)
    print(response.text)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    
    task.completed_at = None
    db.session.commit()

    return jsonify(task.task_response()), 200


#### Goals ####
@goals_bp.route("", methods=["POST","GET"])
def handle_goals():
    if request.method == "POST":
        request_body = request.get_json()
        if 'title' in request_body: 
            new_goal = Goal(title=request_body["title"])

            db.session.add(new_goal)
            db.session.commit()

            goal_response = {
                "id": new_goal.goal_id,
                "title": new_goal.title  
                }
            #new_task_response = new_task.task_response()
            response = {"goal": goal_response}
            return jsonify(response), 201
        else:
            return make_response ({"details": "Invalid data"},400)

    elif request.method == "GET":
        goals = Goal.query.all()
    
        goals_response = []
        for goal in goals:
            # goals_response.append({
            #     "id": goal.goal_id,
            #     "title": goal.title,
            #     })
            goals_response.append(goal.goal_response_lean())
        return jsonify(goals_response),200

@goals_bp.route("/<goal_id>", methods=["GET","PUT","DELETE"])
def handle_goal(goal_id):
    goal = Goal.query.get(goal_id)
   
    if goal is None:
        return make_response("", 404)

    elif request.method == "GET":
        return jsonify(goal.goal_response()), 200

    elif request.method == "PUT":      
        form_data = request.get_json()
        goal.title = form_data["title"]

        db.session.commit()
        
        return jsonify(goal.goal_response()), 200
        
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        delete_text = f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        response = {"details":delete_text}
        return jsonify(response), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET", "POST"])
def handle_goal_tasks(goal_id):
        goal = Goal.query.get(goal_id)

        if goal is None:
            return make_response("", 404)

        elif request.method =="POST":
            request_body = request.get_json()

            for task_id in request_body["task_ids"]:
                tasks = []
                tasks.append(Task.query.get(task_id))

                for task in tasks:
                    task.goal_id = goal_id
                    db.session.commit()

            response = {}
            response["id"] = int(goal_id)
            response["task_ids"] = request_body["task_ids"]

            return jsonify(response), 200

        elif request.method == "GET":
            goal = Goal.query.get(goal_id)
            
            task_dict = []

            for task in goal.tasks:
                task_dict.append({
                    "id": task.task_id,
                    "goal_id": task.goal_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": bool(task.completed_at)

                })

            response = {
                "id": goal.goal_id,
                "title": goal.title,
                "tasks": task_dict
            }

            return jsonify(response), 200
