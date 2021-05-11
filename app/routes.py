from app import db
import requests
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
from sqlalchemy import asc, desc
from datetime import datetime
import os
from dotenv import load_dotenv
from dateutil.parser import parse

load_dotenv()

#################### Routes for Tasks ####################
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():
    order_query = request.args.get("sort")
    if order_query:
        if order_query == "asc":
            tasks = Task.query.order_by(asc(Task.title))
        elif order_query == "desc":
            tasks = Task.query.order_by(desc(Task.title))
        else: 
            raise TypeError("Only asc or desc is accepted here")
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    
    return jsonify(tasks_response), 200
  
@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_single_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return {"task": task.to_json()}, 200
    else:
        return jsonify(None), 404
      

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()
    if all(key in request_body for key in ("title", "description", "completed_at")):
        title = request_body["title"]
        description = request_body["description"]
        completed_at = request_body["completed_at"]
        
        if validate_data(title, description, completed_at): 
            new_task = Task(title = title,
                        description = description,
                        completed_at = completed_at)
            db.session.add(new_task)
            db.session.commit()
            return {
                    "task": new_task.to_json()
            }, 201
    else:
        return {"details": "Invalid data"}, 400
      
def validate_data(title, description, completed_at):
    if type(title) != str or type(description) != str:
        raise TypeError("Title and Description must be in string format") 
    if completed_at is not None:
        try:
            parse(completed_at)
        except:
            raise TypeError("Completed_at must be in the format of datetime")
    return True
      
@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        if validate_data(task.title, task.description, task.completed_at): 
            db.session.commit()
            return {
                    "task": task.to_json()
            }, 200
    else:
        return jsonify(None), 404

@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return {
              "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
        }
    else:
        return jsonify(None), 404
      
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed_at = datetime.utcnow()
        db.session.commit()
        send_slack_notifications(task)
        return {
        "task": task.to_json()
        }, 200
    else:
        return jsonify(None), 404

def send_slack_notifications(task):
    access_token = os.environ.get("AUTH_TOKEN")
    path = "https://slack.com/api/chat.postMessage"
    query_headers = {
          "Authorization": f"Bearer {access_token}"
    }
    query_params = {
          "channel": "task-notifications",
          "text": f"Someone just completed the task {task.title}"
    }
    response = requests.post(path, headers=query_headers, params=query_params)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed_at = None
        db.session.commit()
        return {
        "task": task.to_json()
        }, 200
    else:
        return jsonify(None), 404

#################### Routes for Goals ####################
     
goals_bp = Blueprint("goals", __name__, url_prefix="/goals") 

@goals_bp.route("", methods=["GET"], strict_slashes=False)
def get_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_json())
    
    return jsonify(goals_response), 200
  
@goals_bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
def get_single_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        return {"goal": goal.to_json()}, 200
    else:
        return jsonify(None), 404

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_goal():
    request_body = request.get_json()
    if "title" in request_body:
        new_goal = Goal(title = request_body["title"])
        
        db.session.add(new_goal)
        db.session.commit()

        return {
                "goal": new_goal.to_json()
        }, 201
    else:
        return {"details": "Invalid data"}, 400    
      
@goals_bp.route("/<goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        db.session.delete(goal)
        db.session.commit()
        return {
              "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        }
    else:
        return jsonify(None), 404
      

@goals_bp.route("/<goal_id>", methods=["PUT"], strict_slashes=False)
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        form_data = request.get_json()
        goal.title = form_data["title"]
        db.session.commit()
        return {
                "goal": goal.to_json()
        }, 200
    else:
        return jsonify(None), 404     
      
#################### Routes for Goals-Related-Task ####################
@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def post_tasks_to_goal(goal_id):
    request_body = request.get_json()
    goal = Goal.query.get(goal_id)
    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        task.goal_id = goal_id
    db.session.commit()
    return {
            "id": int(goal_id),
            "task_ids": request_body["task_ids"]
    }, 200
    
@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_goals_tasks(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify(None), 404 
    else:
        tasks = Task.query.filter_by(goal_id=goal_id)
        task_list = []
        for task in tasks:
            task_list.append(task.to_json())
        
    return {"id":int(goal_id),"title":goal.title,"tasks":task_list},200

