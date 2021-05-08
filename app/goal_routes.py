from app import db
from app import helper
from .models.task import Task
from .models.goal import Goal
from flask import request, Blueprint, make_response, jsonify, Response
from sqlalchemy import desc, asc
from datetime import date
import os

#WAVE 5 - CRUD goal 
#create new blueprint for goal
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#WAVE 6 -
@goals_bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def create_goal_tasks(goal_id):
    # get the goal for the specified goal_id
    if not helper.is_int(goal_id):
        return {
            "message": "id must be an integer",
            "success": False
        },400
    
    goal = Goal.query.get(goal_id)
    
    if (goal is None):
        return jsonify(details=f"No Goal found with ID: '{goal_id}'"), 400     
    
    # get the tasks from the request body
    form_data = request.get_json()

    taskids = form_data["task_ids"]

    # get the the tasks with the specified ids
    for tid in taskids:
        task = Task.query.get(int(tid))
        
        if (task is not None):
            task.goal_id = goal_id
            db.session.add(task)    
        else:
            # this handles scenarios where specified TaskId in the request body in invalid / does not exist
            return jsonify(details=f"No Task found with ID: '{tid}'"), 400 
    
    db.session.commit()
    
    return jsonify(id=goal_id, task_ids=taskids), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_goal_tasks(goal_id):
    # get the goal for the specified goal_id
    if not helper.is_int(goal_id):
        return {
            "message": "id must be an integer",
            "success": False
        },400
    
    goal = Goal.query.get(goal_id)
    
    if (goal is None):
        return make_response("", 404)  
    
    related_tasks = []
    
    for task in goal.tasks:
        related_tasks.append(task.to_json())
    
    return jsonify(id=goal_id, title=goal.title, tasks=related_tasks), 200
    

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def create_a_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return jsonify(details="Invalid data"),400
    
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()
    
    return new_goal.to_json_goal(), 201

# WAVE 5
@goals_bp.route("", methods=["GET"], strict_slashes=False)
def get_goals():
    
    goal_list = Goal.query.all()
    
    goal_response = [] 
    for goal in goal_list:
        goal_response.append(goal.to_json_goal_no_key())
    
    return jsonify(goal_response), 200

@goals_bp.route("<goal_id>", methods=["GET"], strict_slashes=False)
def get_one_goal(goal_id):
    
    if not helper.is_int(goal_id):
        return {
            "message": "id must be an integer",
            "success": False
        },400
        
    goal = Goal.query.get(goal_id)
    
    if goal == None:
        return Response("",status=404)
    
    if goal:
        return goal.to_json_goal(), 200
    
 
@goals_bp.route("<goal_id>", methods=["PUT"], strict_slashes=False)
def update_goal(goal_id):
    
    goal = Goal.query.get(goal_id)
    
    if goal == None:
        return Response("", status=404)
    
    if not goal:
        return Response("", status=404)
    
    if goal: 
        form_data = request.get_json()

        goal.title = form_data["title"]

        db.session.commit()

        return goal.to_json_goal(), 200

@goals_bp.route("<goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_goal(goal_id):

    goal = Goal.query.get(goal_id)

    if goal == None:
        return Response("", status=404)

    if goal:
        db.session.delete(goal)
        db.session.commit()
        
        goal_details = f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        
        return jsonify(details=goal_details
                         ),200
        

