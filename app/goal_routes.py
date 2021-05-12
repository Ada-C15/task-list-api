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
def get_goals():
    '''queries all goals from server'''

    goals_query = Goal.query.all()

    return make_response(jsonify([goal.build_dict() for goal in goals_query]))

@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_goal(goal_id):
    '''queries one goal from server using goal_id,
    returns None, 404 using get_or_404 method if goal not found'''

    goal = Goal.query.get_or_404(goal_id)

    return make_response({"goal" : goal.build_dict()}, 200)

@goals_bp.route("", methods = ["POST"])
def post_goal():
    '''posts one goal to database'''

    request_body = request.get_json()
    if "title" not in request_body.keys():
        return make_response({"details": "Invalid data"}, 400)
    new_goal = Goal(
        title=request_body["title"])
    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal":new_goal.build_dict()}, 201)

@goals_bp.route("/<goal_id>", methods = ["PUT"])
def update_goal(goal_id):
    '''updates one goal in database'''

    goal = Goal.query.get_or_404(goal_id)
    form_data = request.get_json()
    goal.title = form_data["title"]
    db.session.commit()

    return make_response(jsonify({"goal":goal.build_dict()}))

@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_goal(goal_id):
    '''deletes one goal in database'''

    goal = Goal.query.get_or_404(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return make_response({"details" : f'Goal {goal_id} \"{goal.title}\" successfully deleted'})

@goals_bp.route("/<goal_id>/tasks", methods = ["POST"])
def add_tasks_to_goals(goal_id):
    '''adds tasks to goals,
    returns goal and associated task ids using list comprehension'''

    goal = Goal.query.get_or_404(goal_id)
    request_body = request.get_json(goal)
    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        task.goal_id = goal_id
        
    db.session.commit()

    return make_response(jsonify({"id": goal.goal_id, "task_ids": [task.task_id for task in goal.tasks]}))

@goals_bp.route("/<goal_id>/tasks", methods = ["GET"])
def get_tasks_for_goal(goal_id):
    '''gets all tasks associated with one goal,
    returns a goal and task dictionaries using list comprehension'''

    goal = Goal.query.get_or_404(goal_id)
    tasks = [task.build_dict() for task in goal.tasks]
    goal_dict = goal.build_dict()
    goal_dict["tasks"] = tasks

    return make_response(goal_dict)