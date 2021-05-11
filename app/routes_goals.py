from flask import Blueprint, request, jsonify, make_response
from app import db 
from app.models.goal import Goal 
from app.models.task import Task 
from sqlalchemy import asc, desc

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["GET"], strict_slashes=False)
def get_goals():
    goals = Goal.query.all() 
    
    goals_response = [] 
    for goal in goals: 
        goals_response.append(goal.goals_to_json())

    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
def get_one_goal(goal_id):
    goal = Goal.query.get(goal_id)
    
    if goal: 
        return jsonify(goal.specific_goal_to_json()), 200
    
    return make_response("", 404)

@goals_bp.route("", methods=["POST"], strict_slashes=False)
def post_goal(): 
    request_body = request.get_json()
    if request_body.get("title"):  
        new_goal = Goal(title=request_body["title"])

        db.session.add(new_goal)
        db.session.commit() 
        return jsonify(new_goal.specific_goal_to_json()), 201
    
    return {"details": "Invalid data"}, 400

@goals_bp.route("<goal_id>", methods=["PUT"], strict_slashes=False)
def update_goal(goal_id): 
    goal = Goal.query.get(goal_id)
    
    if goal: 
        update_data = request.get_json() 
        goal.title = update_data["title"]
    
        db.session.commit()
        return jsonify(goal.specific_goal_to_json()), 200
    
    return make_response("", 404)

@goals_bp.route("<goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal: 
        db.session.delete(goal)
        db.session.commit()
        
        return {
            "details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"
        }, 200 
    
    return make_response("", 404)

@goals_bp.route("<int:goal_id>/tasks", methods=["POST"], strict_slashes=False)
def post_list_of_tasks(goal_id):
    request_body = request.get_json()
    if request_body.get("task_ids"):  
        task_ids = request_body["task_ids"]
        for task_id in task_ids: 
            task = Task.query.get(task_id)
            task.goal_id = goal_id
            db.session.commit() 
        return jsonify({"id": goal_id, "task_ids":task_ids}), 200
    
    return make_response("", 404)

@goals_bp.route("<int:goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_list_of_tasks(goal_id): 
    goal = Goal.query.get(goal_id)
    
    if goal: 
        task = Task.query.get(goal_id)
        if task: 
            return jsonify(goal.goal_associated_tasks(task)), 200 
        return jsonify(goal.goal_associated_tasks(task)), 200
    
    return make_response("", 404)

    