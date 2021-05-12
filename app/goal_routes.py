from flask import Blueprint
from app.models.goal import Goal
from app import db
from flask import request, Blueprint, make_response, Response, jsonify
from datetime import date
import requests
from secrets import slack_token

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["GET", "POST"])
def handle_tasks():  # NameError
    if request.method == "GET":

        goals = Goal.query.all()
        goals_response = []

        for goal in goals:
            goals_response.append({
                "id": goal.goal_id,
                "title": goal.title
            })
        return jsonify(goals_response)
     

    elif request.method == "POST":  # CRUD CREATE
        # check for request body title and description, plus ensure both are strings
        request_body = request.get_json()

        if "title" not in request_body:
            return {
                "goal": f"Invalid title"
            }, 400

        goal = Goal(
            title=request_body["title"]
        )

        db.session.add(goal)
        db.session.commit()

        return {
            "goal": {
                "id": goal.goal_id,
                "title": goal.title
            }
        }, 201

#get 1 goal
@goal_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def handle_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal == None:
        return make_response(f"Goal{goal_id} not found", 404)

    if request.method == "GET":
        return {
            "goal": {
                "id": goal.goal_id,
                "title": goal.title
            }
        }
    elif request.method == "PUT":
        form_data = request.get_json()

        goal.title = form_data["title"]

        db.session.commit()

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        
        return {
            "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        }

@goal_bp.route("/<goal__id>/mark_complete", methods=["PATCH"])
def mark_complete(goal_id):
    goal = Goal.query.get(goal_id)

    if goal == None:
        return "",404

    db.session.commit()

    r = requests.post(f"https://slack.com/api/chat.postMessage?channel=goal-notifications&text=Someone just completed the goal {goal.title}", headers={"Authorization":slack_token})

    return {
        "goal": {
            "id": goal.goal_id,
            "title": "Updated Goal Title"
        }
    }

@goal_bp.route("/<goal_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(goal_id):
    goal = Goal.query.get(goal_id)
    
    if goal == None:
        return "",404

    # goal.completed_at = None

    db.session.commit()

    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }
    }