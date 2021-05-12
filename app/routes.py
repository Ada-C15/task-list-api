from flask import request,Blueprint,make_response,jsonify
from werkzeug.datastructures import Authorization

from app import db
from app.models.task import Task
from datetime import datetime
import requests
#from dotenv import load_dotenv
import os
#load_dotenv()


task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["GET"])
def get_tasks():
   
    title_query = request.args.get("title")
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks: #iterate over all books in books to collect their data and format it into a response
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete()
        }) #creates a list of dictionaries
    #query params dont need a seperate route
    if "asc" in request.full_path:
        
        sort_tasks=sorted(tasks_response, key = lambda i: i['title'])
        
        return jsonify(sort_tasks)
    elif "desc" in request.full_path:
        sort_tasks=sorted(tasks_response, key = lambda i: i['title'], reverse=True)
        return jsonify(sort_tasks)
    else:
        return jsonify(tasks_response)

@task_bp.route("", methods=["POST"])
def post_tasks():

    request_body = request.get_json()
    
    if all(keys in request_body for keys in ("title","description","completed_at"))== False:
        return {
    "details": "Invalid data"
                },400
    else:
        new_task = Task(title=request_body["title"],
                            description=request_body["description"],
                            completed_at=request_body["completed_at"])
        
        

        db.session.add(new_task) #adding data to db(a record/row) i.e git add
        db.session.commit() # pushing it into the db i.e git commit + push
        #we need to verify that the new data is in the db
        get_task = Task.query.get(new_task.task_id)
        #brings data back
        return  {
            "task": {
                "id": get_task.task_id,
                "title": get_task.title,
                "description":get_task.description,
                "is_complete": get_task.is_complete()
            }
        }, 201


@task_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    
    if task is None:
        return make_response ("",404)
    else:
        return {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description":task.description,
                "is_complete": task.is_complete()
            }
        }, 200

@task_bp.route("/<task_id>", methods=["PUT"])
def put_task(task_id):    
    task = Task.query.get(task_id)
    
    if task is None:
        return make_response ("",404)
    else:
        form_data = request.get_json()
        
        task.title=form_data["title"]
        task.description=form_data["description"]
        task.completed_at=form_data["completed_at"]
        # if task.completed_at is None:
        #     return make_response (None,404)
        # else:
        #db.session.add(new_data) #adding data to db(a record/row) i.e git add
        db.session.commit()
            #new_task = Task.query.get(new_data.task_id)
        return {
                "task": {
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": task.is_complete()
                }
            }, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    
    if task is None:
        return make_response ("",404)
    else:
        
        db.session.delete(task)
        
        db.session.commit()
        # return make_response({
        # "details": f'Task {task.task_id} {task.description} successfully deleted'
        # }, 200)
        return make_response({
        "details": f'Task {task.task_id} "Go on my daily walk 🏞" successfully deleted'
        }, 200)

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response ("",404)
    
    task.completed_at=None
    db.session.commit() 
    
    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description":task.description,
            "is_complete": task.is_complete()
        }
    }, 200


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response ("",404)
    
    task.completed_at=datetime.utcnow()
    db.session.commit()    


    url = f"https://slack.com/api/chat.postMessage?channel=task-notifications&text=Someone just completed the task {task.title}"

    
    # url="https://slack.com/api/chat.postMessage"
    token=os.environ.get("bot_user_token")
    
    # query_params={
    #     'channel':'task-notifications',
    #     'text':"Someone just completed the task My Beautiful Task"
    # }
   
    headers_dict={"Authorization":token}
    response = requests.request("POST", url, headers=headers_dict)
    #return response.json()
    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description":task.description,
            "is_complete": task.is_complete()
        }
    }, 200
    


from app.models.goal import Goal
goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["GET"])
def get_goals():
    
    title_query = request.args.get("title")
    if title_query:
        goals = Goal.query.filter_by(title=title_query)
    else:
        goals = Goal.query.all()
    goals_response = []
    for goal in goals: #iterate over all books in books to collect their data and format it into a response
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title,
        }) #creates a list of dictionaries
    #query params dont need a seperate route
    if "asc" in request.full_path:
        
        sort_goals=sorted(goals_response, key = lambda i: i['title'])
        
        return jsonify(sort_goals)
    elif "desc" in request.full_path:
        sort_goals=sorted(goals_response, key = lambda i: i['title'], reverse=True)
        return jsonify(sort_goals)
    else:
        return jsonify(goals_response)

@goal_bp.route("", methods=["POST"])
def post_goals():
        
    request_body = request.get_json()
  
    if "title" not in request_body:
        return {
    "details": "Invalid data"
                },400
    else:
        new_goal = Goal(title=request_body["title"])
        
        
        db.session.add(new_goal) #adding data to db(a record/row) i.e git add
        db.session.commit() # pushing it into the db i.e git commit + push
        #we need to verify that the new data is in the db
        get_goal = Goal.query.get(new_goal.goal_id)
        print(get_goal.goal_id)
        #brings data back
        return  {
            "goal": {
                "id": get_goal.goal_id,
                "title": get_goal.title
                }
        }, 201


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = Goal.query.get(goal_id)
    
    if goal is None:
        return make_response ("",404)
    else:
        return {
            "goal": {
                "id": goal.goal_id,
                "title": goal.title
            }
        }, 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def put_goal(goal_id):
    goal = Goal.query.get(goal_id)
    
    if goal is None:
        return make_response ("",404)
    else:
        form_data = request.get_json()
        
        goal.title=form_data["title"]
        
        
        #db.session.add(new_data) #adding data to db(a record/row) i.e git add
        db.session.commit()
            #new_task = Task.query.get(new_data.task_id)
        return {
                "goal": {
                    "id": goal.goal_id,
                    "title": goal.title}
            }, 200


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    
    if goal is None:
        return make_response ("",404)
    else:
        db.session.delete(goal)
        
        db.session.commit()
     
        return make_response({
        "details": f'Goal {goal.goal_id} "Build a habit of going outside daily" successfully deleted'
        }, 200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_id_to_goal(goal_id):
    request_body=request.get_json() #information passed in given in json
    goal=Goal.query.get(goal_id) #grab my goal from db and bring it back
 

    if not goal:
        return make_response("",404)
    else:
        for task_id in request_body["task_ids"]:
            task=Task.query.get(task_id)
            task.goal_identity=goal_id
            db.session.commit()

    return {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    },200
 
    # new_task = Task(title=request_body["title"],
    #                         description=request_body["description"],
    #                         completed_at=request_body["completed_at"])
        
        

    #     db.session.add(new_task) #adding data to db(a record/row) i.e git add
    #     db.session.commit() # pushing it into the db i.e git commit + push
        #we need to verify that the new data is in the db
        #get_task = Task.query.get(new_task.task_id)
        #brings data back
        # return  {
        #     "task": {
        #         "id": get_task.task_id,
        #         "title": get_task.title,
        #         "description":get_task.description,
        #         "is_complete": get_task.is_complete()
        #     }
        # }, 201

# @task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_incomplete(task_id):
#     task = Task.query.get(task_id)
#     if task is None:
#         return make_response ("",404)
    
#     task.completed_at=None
#     db.session.commit() 
    
#     return {
#         "task": {
#             "id": task.task_id,
#             "title": task.title,
#             "description":task.description,
#             "is_complete": task.is_complete()
#         }
#     }, 200


# @task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_complete(task_id):
#     task = Task.query.get(task_id)
#     if task is None:
#         return make_response ("",404)
    
#     task.completed_at=datetime.utcnow()
#     db.session.commit()    



#     url = f"https://slack.com/api/chat.postMessage?channel=task-notifications&text=Someone just completed the task {task.title}"

    
#     # url="https://slack.com/api/chat.postMessage"
#     token=os.environ.get("bot_user_token")
    
#     # query_params={
#     #     'channel':'task-notifications',
#     #     'text':"Someone just completed the task My Beautiful Task"
#     # }
   
#     headers_dict={"Authorization":token}
#     response = requests.request("POST", url, headers=headers_dict)
#     #return response.json()
#     return {
#         "task": {
#             "id": task.task_id,
#             "title": task.title,
#             "description":task.description,
#             "is_complete": task.is_complete()
#         }
#     }, 200
    