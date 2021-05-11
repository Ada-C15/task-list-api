
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
import datetime
import os 
import requests

goal_bp = task_bp = Blueprint("goal", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["GET", "POST"], strict_slashes=False)

def handle_goal():

    if request.method == "GET":

        goals = Goal.query.all()
        response = []

        if not goals:
            return jsonify(response), 200


        for goal in goals:
            response.append({
                "id": goal.goal_id,
                "title": goal.title
            })
        
        return jsonify(response), 200
    
    elif request.method == "POST":

        request_body = request.get_json()

        if request_body:
            new_goal = Goal(title=request_body["title"])

            db.session.add(new_goal)
            db.session.commit()

            goal_response = {
                    "id": new_goal.goal_id,
                    "title": new_goal.title
                    }
            dict_copy = goal_response.copy()
            response = {"goal": dict_copy}

            return jsonify(response), 201
        
        else: 
            response = {"details": "Invalid data"}
            return jsonify(response), 400


@goal_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])

def get_one_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404

    elif request.method == "GET":

        goal_response = {
                "id": goal.goal_id,
                "title": goal.title,
                }

        dict_copy = goal_response.copy()
        response = {"goal": dict_copy}

        return jsonify(response), 200
    
    elif request.method == "PUT":

        form_data = request.get_json()

        goal.title = form_data["title"]

        db.session.commit()

        goal_response = {
                "id": goal.goal_id,
                "title": goal.title
                }

        dict_copy = goal_response.copy()
        response = {"goal": dict_copy}

        return jsonify(response), 200
    
    elif request.method == "DELETE":

        db.session.delete(goal)
        db.session.commit()

        text = f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        
        response = {"details": text}

        return jsonify(response), 200 

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])

def handle_goal_tasks(goal_id):

        goal = Goal.query.get(goal_id)

        if goal is None:
            return jsonify(None), 404

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

                









task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["GET", "POST"], strict_slashes=False)

def handle_task():

    if request.method == "GET":

        sort_by_title = request.args.get("sort")

        if sort_by_title == "asc": 
            # sorted_asc = sorted(tasks_response, key = lambda i: i["title"])
            tasks = Task.query.order_by(Task.title.asc())
            
        elif sort_by_title == "desc":
            # sorted_desc = sorted(tasks_response, key = lambda i:i["title"], reverse = True)
            tasks = Task.query.order_by(Task.title.desc())
                
        else:
            tasks = Task.query.all()

        tasks_response = []

        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            })

        return jsonify(tasks_response)

    elif request.method == "POST":

        request_body = request.get_json()

        if all(key in request_body for key in ("title", "description", "completed_at")):
            new_task = Task(title=request_body["title"],
                description=request_body["description"],
                completed_at=request_body["completed_at"])

            db.session.add(new_task)
            db.session.commit()

            tasks_response = {
                    "id": new_task.task_id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": bool(new_task.completed_at)
                    }
            dict_copy = tasks_response.copy()
            response = {"task": dict_copy}

            return jsonify(response), 201
        
        else:
            response = {"details": "Invalid data"}
            return jsonify(response), 400
        

    
@task_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])

def get_one_task(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404
        
    elif request.method == "GET":

        tasks_response = {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
                }
        dict_copy = tasks_response.copy()
        response = {"task": dict_copy}

        return jsonify(response)

    elif request.method == "PUT":

        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at=form_data["completed_at"]

        db.session.commit()

        tasks_response = {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
                }

        dict_copy = tasks_response.copy()
        response = {"task": dict_copy}

        return jsonify(response), 200
    
    elif request.method == "DELETE":

        db.session.delete(task)
        db.session.commit()

        text = f"Task {task.task_id} \"{task.title}\" successfully deleted"
        
        response = {"details": text}

        return jsonify(response), 200 

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])

#params: channel: task-notifications, text: text
#headers: Authorization: Bearer xoxb-2044330967011-2041081116293-8MePJn0y44PiQcOHslsL2Jh6
#channel id: C1234567890
#method URL https://slack.com/api/chat.postMessage

def mark_complete(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    elif request.method == "PATCH":

        task.completed_at = datetime.datetime.now()

        db.session.commit()

        #the slack way: this worked!

        # client=WebClient(token=os.environ.get("SLACK_AUTHORIZATION_TOKEN"))

        # channel_id="C020VA8FNSK"

        # result = client.chat_postMessage(channel=channel_id, text=f"Someone just completed the task {task.title}")

        SLACK_BOT_TOKEN = os.environ.get("SLACK_AUTHORIZATION_TOKEN")
        headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
        url = "https://slack.com/api/chat.postMessage"
        params = dict(
                channel="C020VA8FNSK",
                text=f"Someone just completed the task {task.title}")
        
        req = requests.request("POST", url, params=params, headers=headers)

        tasks_response = {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
                }

        dict_copy = tasks_response.copy()
        response = {"task": dict_copy}

        return jsonify(response), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])

def mark_incomplete(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return jsonify(None), 404

    elif request.method == "PATCH":

        task.completed_at = None

        db.session.commit()

        tasks_response = {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
                }

        dict_copy = tasks_response.copy()
        response = {"task": dict_copy}

        return jsonify(response), 200






