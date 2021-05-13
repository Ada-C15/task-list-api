# Task List API Project
# Katrina Kimzey
# Cohort 15 - Paper

from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from datetime import datetime
import os 
from dotenv import load_dotenv

tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")

load_dotenv()
slack_path = 'https://slack.com/api/chat.postMessage'

# ============== All Tasks ========================

@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        direction = request.args.get("sort")
        if direction == "asc":
            tasks = Task.query.order_by(asc("title"))
        elif direction == "desc":
            tasks = Task.query.order_by(desc("title"))
        else:
            tasks = Task.query.all()

        tasks_response = [task.to_dict() for task in tasks]

        return jsonify(tasks_response)

    elif request.method == "POST":
        request_body = request.get_json()
        try:
            new_task = Task(title=request_body["title"],
                            description=request_body["description"],
                            completed_at=request_body["completed_at"]
                            )
        except KeyError:
            return make_response({"details": "Invalid data"}, 400)

        db.session.add(new_task)
        db.session.commit()

        return make_response({"task" : new_task.to_dict()}, 201)

# ==================== Task by id ==============================

@tasks_bp.route("/<active_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(active_id):
    task = Task.query.get_or_404(active_id)

    if request.method == "GET":
        return {"task" : task.to_dict()}

    elif request.method == "PUT":
        update_data = request.get_json()

        task.title = update_data["title"]
        task.description = update_data["description"]
        task.completed_at = update_data["completed_at"]

        db.session.commit()

        return {"task" : task.to_dict()}

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return jsonify({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"})

# ================= Task by id change completeness ======================
import requests

@tasks_bp.route("/<active_id>/mark_complete", methods=["PATCH"])
def update_to_complete(active_id):
    task = Task.query.get_or_404(active_id)

    task.completed_at = datetime.now()
    db.session.commit()

    slack_payload = {"channel" : "task-notifications",
                    "text" : f"Someone just completed the task {task.title}"
                    }
    slack_header = {"Authorization" : os.environ.get("SLACKBOT_API_AUTH")}
    slack_response = requests.post(slack_path, headers=slack_header, params=slack_payload)

    return {"task" : task.to_dict()}

@tasks_bp.route("/<active_id>/mark_incomplete", methods=["PATCH"])
def update_to_incomplete(active_id):
    task = Task.query.get_or_404(active_id)

    task.completed_at = None
    db.session.commit()

    return {"task" : task.to_dict()}

# ================================================================
# =========================== GOALS ==============================

goals_bp = Blueprint("goal", __name__, url_prefix="/goals")

# =============== All goals ======================================

@goals_bp.route("", methods=["GET", "POST"])
def handle_goals():
    if request.method == "GET":
        direction = request.args.get("sort")
        if direction == "asc":
            goals = Goal.query.order_by(asc("title"))
        elif direction == "desc":
            goals = Goal.query.order_by(desc("title"))
        else:
            goals = Goal.query.all()

        goals_response = [goal.to_dict() for goal in goals]

        return jsonify(goals_response)

    elif request.method == "POST":
        request_body = request.get_json()
        try:
            new_goal = Goal(title=request_body["title"])
        except KeyError:
            return make_response({"details": "Invalid data"}, 400)

        db.session.add(new_goal)
        db.session.commit()

        return make_response({"goal" : new_goal.to_dict()}, 201)

# ============= Goal by id ==================================

@goals_bp.route("/<active_id>", methods=["GET", "PUT", "DELETE"])
def handle_goal(active_id):
    goal = Goal.query.get_or_404(active_id)

    if request.method == "GET":
        return {"goal" : goal.to_dict()}

    elif request.method == "PUT":
        update_data = request.get_json()
        goal.title = update_data["title"]

        db.session.commit()

        return {"goal" : goal.to_dict()}

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return jsonify({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"})

# ============= Goal with tasks =============================

@goals_bp.route("/<active_id>/tasks", methods=["GET", "POST"])
def handle_tasks_under_goal(active_id):
    goal = Goal.query.get_or_404(active_id)

    if request.method == "GET":
        dict_response = goal.to_dict()

        matching_tasks = Task.query.filter_by(goal_id=active_id)
        task_list = [task.to_dict() for task in matching_tasks]
        dict_response["tasks"] = task_list

        return dict_response

    elif request.method == "POST":
        request_data = request.get_json()

        for task_id in request_data["task_ids"]:
            task = Task.query.get_or_404(task_id)
            task.goal_id = goal.goal_id

        db.session.commit()
        return {"id" : goal.goal_id, "task_ids" : request_data["task_ids"]}
