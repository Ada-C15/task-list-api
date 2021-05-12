from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime
import os, requests

tasks_bp = Blueprint("tasks",__name__,url_prefix="/tasks")
goals_bp = Blueprint("goals",__name__,url_prefix="/goals")

#wave1
@tasks_bp.route("", methods=["POST","GET"], strict_slashes = False)
def handle_tasks():

    if request.method == "POST":
        request_body = request.get_json()
        
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body: 
            return ({"details":"Invalid data"},400)
        else:
            task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at =request_body["completed_at"])
            db.session.add(task)
            db.session.commit()

            return make_response({"task":task.to_json()},201)
    else:
        title_sort_query = request.args.get("sort")
        if title_sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        elif title_sort_query == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        else:
            tasks = Task.query.all()

        tasks_response = []
        for task in tasks:
                tasks_response.append(task.to_json())

        return jsonify(tasks_response)

#wave2
@tasks_bp.route("/<task_id>", methods=["GET","PUT","DELETE","PATCH"], strict_slashes = False)
def handle_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response(" ", 404)
    
    if request.method == "GET":
        return make_response({"task":task.to_json()},200)

    elif request.method == "PUT":
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()

        return make_response({"task":task.to_json()},200)

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()

        return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})

#wave 3 & 4
@tasks_bp.route("/<task_id>/<mark_status>", methods=["PATCH"], strict_slashes = False)
def mark_completed(task_id,mark_status):
    task = Task.query.get(task_id)
    if not task:
        return make_response(" ", 404)

    elif mark_status == "mark_complete":
        task.completed_at = datetime.utcnow()
        db.session.commit()
        an_external_web_api_url = "https://slack.com/api/chat.postMessage"
        slack_api_key = os.environ.get("MY_SLACK_API")
        my_headers = {"Authorization":f"Bearer {slack_api_key}"}
        task_params ={
            "channel":"task-notifications",
            "text":f"Someone just completed the task {task.title}"}
        response = requests.post(an_external_web_api_url, params=task_params, headers=my_headers )
        
        return make_response({"task":task.to_json()},200)

    elif mark_status == "mark_incomplete":
        task.completed_at = None
        db.session.commit()
        
        return make_response({"task":task.to_json()},200)

#wave5
@goals_bp.route("", methods=["POST","GET"], strict_slashes = False)
def handle_goals():
    
    if request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body: 
            return ({"details":"Invalid data"},400)
        else:
            goal = Goal(title=request_body["title"])
            db.session.add(goal)
            db.session.commit()
            
            return make_response({"goal":goal.goals_to_json()},201)

    else:
        goals = Goal.query.all()
        goals_response = []
        for goal in goals:
                goals_response.append(goal.goals_to_json())

        return jsonify(goals_response)


@goals_bp.route("/<goal_id>", methods=["GET","PUT","DELETE","PATCH"], strict_slashes = False)
def handle_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response(" ", 404)

    if request.method == "GET":
        return make_response({"goal":goal.goals_to_json()},200)

    elif request.method == "PUT":
        form_data = request.get_json()
        goal.title = form_data["title"]
        db.session.commit()

        return make_response({"goal":goal.goals_to_json()},200)

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()

        return make_response({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'})

#wave6
@goals_bp.route("/<goal_id>/tasks",methods=["POST","GET"], strict_slashes = False)
def create_goals_tasks(goal_id):
    if request.method=="POST":
        request_body = request.get_json()
        for task_id in request_body["task_ids"]:
            task = Task.query.get(task_id)
            task.goal_id = goal_id
        db.session.commit()

        return {"id":task.goal_id,"task_ids":request_body["task_ids"]}

    else:
        goal = Goal.query.get(goal_id)
        if not goal:
            return make_response("",404)
        else:
            num = int(goal_id)
            tasks = Task.query.filter_by(goal_id=num)
            tasks_list =[]
            for task in tasks:
                tasks_list.append(task.to_json())
                
            return {"id":num,"title":goal.title,"tasks":tasks_list},200


    



    