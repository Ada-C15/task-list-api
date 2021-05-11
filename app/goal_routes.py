import requests
from app import db
from flask import request, Blueprint, make_response, jsonify
from app.models.task import Task
from app.models.goal import Goal
from dotenv import load_dotenv
import os


load_dotenv()

goals_bp = Blueprint("goals", __name__, url_prefix="/goals") 

@goals_bp.route("", methods = ["GET"])
def handle_goals():
    goals_query = Goal.query.all()
    goals_response = []
    for goal in goals_query:
        goals_response.append(goal.build_dict())
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)
    else:
        return ({"goal" : goal.build_dict()}, 200)

@goals_bp.route("", methods = ["POST"])
def post_goal():
    request_body = request.get_json()
    if "title" not in request_body.keys():
        return make_response({"details": "Invalid data"}, 400)
    new_goal = Goal(
        title=request_body["title"])
    db.session.add(new_goal)
    db.session.commit()
    return {"goal":new_goal.build_dict()}, 201

@goals_bp.route("/<goal_id>", methods = ["PUT"])
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)
    form_data = request.get_json()
    goal.title = form_data["title"]
    db.session.commit()

    return make_response(jsonify({"goal":goal.build_dict()}))

@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)
    db.session.delete(goal)
    db.session.commit()

    return {"details" : f'Goal {goal_id} \"{goal.title}\" successfully deleted'}

@goals_bp.route("/<goal_id>/tasks", methods = ["POST"])
def add_tasks_to_goals(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        request_body = request.get_json(goal)
        for task_id in request_body["task_ids"]:
            task = Task.query.get(task_id)
            task.goal_id = goal_id

        db.session.commit()

        return make_response(jsonify({"id": goal.goal_id, "task_ids": [task.task_id for task in goal.tasks]}))

@goals_bp.route("/<goal_id>/tasks", methods = ["GET"])
def get_tasks_for_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)
    tasks = [task.build_dict() for task in goal.tasks]
    goal_dict = goal.build_dict()
    goal_dict["tasks"] = tasks
    return goal_dict