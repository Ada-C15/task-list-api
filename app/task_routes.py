import requests
from app import db
from flask import request, Blueprint, make_response, jsonify
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc, asc
from dotenv import load_dotenv
import os
from app.slack_bot import slack_message
from datetime import datetime

load_dotenv()
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods = ["GET"])
def get_tasks():
    '''gets all tasks from database, sorting by asc or desc'''

    order = request.args.get("sort")
    if order == "asc":
        tasks_query = Task.query.order_by(Task.title)
    else:
        tasks_query = Task.query.order_by(Task.title.desc())
    return make_response(jsonify([task.build_dict() for task in tasks_query]), 200)


@tasks_bp.route("", methods = ["POST"])
def add_tasks():
    '''adds tasks to db, verifying all necessary fields are present
    sends notification to slack using slack_message'''

    request_body = request.get_json()
    if "title" not in request_body.keys() or "description" not in request_body.keys() or "completed_at" not in request_body.keys():
        return make_response({"details": "Invalid data"}, 400)
        
    new_task = Task(
        title=request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"],
    )
    # slack_message(f"Someone just added {new_task.title} to the task list.")
    db.session.add(new_task)
    db.session.commit()

    return make_response({"task":new_task.build_dict()}, 201)


@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_task(task_id):
    '''retrieves single task from db'''

    task = Task.query.get_or_404(task_id)

    return make_response(jsonify({"task":task.build_dict()}))
        

@tasks_bp.route("/<task_id>", methods = ["PUT"])
def update_task(task_id):
    '''takes in new values from query,
    updates a single task'''

    task = Task.query.get_or_404(task_id)
    form_data = request.get_json()
    task.title = form_data["title"]
    task.description = form_data["description"]
    task.completed_at = form_data["completed_at"]

    db.session.commit()

    return make_response({"task":task.build_dict()})

@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    '''deletes a single task from db'''

    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task_id} \"{task.title}\" successfully deleted"})
    
@tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def mark_complete(task_id):
    '''marks task as a complete,
    populates completed_at with current date/time,
    sends notification in slack'''

    task = Task.query.get_or_404(task_id)
    task.completed_at = datetime.now()
    slack_message(f"Someone just completed {task.title}.")
    db.session.commit()
    
    return make_response({"task": task.build_dict()}, 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def mark_incomplete(task_id):
    '''marks task incomplete, 
    resets completed_at to None'''

    task = Task.query.get_or_404(task_id)
    if task.completed_at:
        task.completed_at = None
        
    return make_response({"task": task.build_dict()}, 200)

