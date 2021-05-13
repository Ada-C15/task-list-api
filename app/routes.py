from app import db
from .models.task import Task
from .models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime 
import requests
import os 

task_bp = Blueprint("task", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

#endpoint for new task entry post method 
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    #checks to see if 'title' is found as a key in request_body called 'validation'
    if 'title' not in request_body:
        return make_response(jsonify({"details":"Invalid data"}), 400)
    if 'description' not in request_body:
        return make_response(jsonify({"details":"Invalid data"}), 400)
    # checking to see if key exists in the dictionary
    if 'completed_at' not in request_body:
        return make_response(jsonify({"details":"Invalid data"}), 400)
    # checking to see what the value is in the completed_at key 
    if request_body["completed_at"] is None:
        completed_date = None
    
    else:
       # i am providing the format that the string date is currently in so the built in function can return it back in the correct format
       completed_date = datetime.strptime(request_body["completed_at"],'%a, %d %b %Y %H:%M:%S GMT')

    new_task = Task(
        title = request_body["title"], 
        description = request_body["description"],
        completed_at = completed_date
    )
    
    db.session.add(new_task)
    db.session.commit()
        
    return jsonify({
    "task": new_task.to_json()
    }), 201


#endpoint for getting tasks
@task_bp.route("", methods=["GET"])
def tasks():
    
    # grabbing sort query parameter and its value ex. sort=asc from the client request and storing it in local variable
    sort_titles = request.args.get('sort')
    # if sort query param is in the body request of the user, we need to now check what the value of sort parameter. If value is set to sort=asc then.... else if sort=desc do...
    #if sorts value == asc then ....
    task_response = []
    if sort_titles:
        if sort_titles == "asc":
            task_by_asc = Task.query.order_by(Task.title.asc())
            for task in task_by_asc:
                task_response.append(task.to_json())   
        
        if sort_titles == 'desc':
            task_by_desc = Task.query.order_by(Task.title.desc())
            for task in task_by_desc:
                task_response.append(task.to_json())
        
        return jsonify(task_response), 200
    
    else:
        tasks = Task.query.all()
        task_response = []
        for task in tasks:
            #using to_json helper function 
            task_response.append(task.to_json())
        return jsonify(task_response), 200


#endpoint to get response body by task_id
@task_bp.route("/<task_id>", methods=["GET","PUT","DELETE"],)
def task(task_id):
    task = Task.query.get(task_id)
    # if task is not found
    if not task:
        return '',404
    
    #checking to see if task has goal_id
    if request.method == "GET":
        if task.goal_id:
            return {"task": task.to_json_goal_id()}
        else:
            return {"task":task.to_json()},200
    
    if request.method =='PUT':
        request_body = request.get_json()
        #assigning updated values to a task instance
        task.title = request_body['title']
        task.description = request_body['description']
        task.completed_at = request_body['completed_at']
        db.session.commit()
        return jsonify(task=task.to_json()), 200

    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify(details=f'Task {task.task_id} "{task.title}" successfully deleted'),200


    

#endpoint for giving completed_at attribute column with a datetime value in the DB. route parameter is mark_complete
@task_bp.route("<task_id>/mark_complete",methods=["PATCH"])
def complete(task_id):
    task = Task.query.get(task_id)
    if not task:
        return '', 404 
    # in order to make variable truthy we need to have datatype as value
    task.completed_at = datetime.utcnow()
    db.session.commit()
    
    call_slack(task)
    
    return make_response({"task": task.to_json()}, 200)#helper function to 

#call slack api helper function    
def call_slack(task):
    #using os package from __init__.py to pull value for the argument passed in 
    key = os.environ.get("API_KEY")
    url = "https://slack.com/api/chat.postMessage"
    slack_str = f"Someone just completed the task {task.title}"
    requests.post(url,data={"token": key ,"channel": "general" , "text": slack_str})
    



#endpoint for giving completed_at column/attribute the value null/NONE in the DB. route parameter is mark_incomplete
@task_bp.route("<task_id>/mark_incomplete",methods=["PATCH"])
def in_complete(task_id):
    task = Task.query.get(task_id)
    if not task:
        return '', 404    
    task.completed_at = None 
    db.session.commit()
    return make_response({"task": task.to_json()}, 200)

#endpoint for creating a new goal
@goal_bp.route("",methods=["POST"])
def create_goal():
    request_body = request.get_json()
    #checks to see if 'title' is found as a key in request_body called 'validation'
    if 'title' not in request_body:
        return make_response(jsonify({"details":"Invalid data"}), 400)

    new_goal = Goal(title = request_body["title"]) 
       
    db.session.add(new_goal)
    db.session.commit()
        
    return jsonify({
    "goal": new_goal.goal_to_json()
    }), 201

#endpont for GET, PUT, DELETE based on goal_id
@goal_bp.route("/<goal_id>", methods=["GET","PUT","DELETE"],)
def handle_goal(goal_id):
    goal = Goal.query.get(goal_id)
    # if task is not found
    if not goal:
        return '',404
    #
    if request.method == "GET":
        return jsonify(goal=goal.goal_to_json()), 200
   
    
    if request.method =='PUT':
        request_body = request.get_json()
        #assigning updated values to task
        goal.title = request_body['title']
    
        db.session.commit()
        return jsonify(goal=goal.goal_to_json()), 200

    if request.method == 'DELETE':
        db.session.delete(goal)
        db.session.commit()
        return jsonify(details=f'Goal {goal.goal_id} "{goal.title}" successfully deleted'),200

# GET method to return all goals
@goal_bp.route('', methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.goal_to_json())
    return jsonify(goals_response)



# POST endpoint to add list of task_ids to one goal
@goal_bp.route("/<goal_id>/tasks",methods=["POST"])
def tasks_to_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return '',404
    # request body has a goal and list of tasks to assign to that goal
    request_body = request.get_json()
    # request_body looks like {'tasks': [1,2]}  value of tasks refers to the task_id columm of Task 

    for task_id in request_body['task_ids']:
        task = Task.query.get(task_id)
        if task not in goal.tasks:
            goal.tasks.append(task)
            
    
    db.session.commit()
    
    return make_response({"id": int(goal_id), "task_ids": request_body["task_ids"]}, 200)                                                                          

#GET route to return tasks of a specific goal                
@goal_bp.route("/<goal_id>/tasks",methods=["GET"])
def get_goal_tasks(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return '',404
    # request body contains a goal object with given goal_id
    
    list_of_tasks = []
    #tasks is referring to our tasks attribute in Goal#
    for task in goal.tasks:
        list_of_tasks.append(task.to_json_goal_id())
        #goal.task(helper function with goal_id as a key)
    
    return jsonify(id=int(goal_id),title=goal.title,tasks=list_of_tasks), 200

