from flask import request,Blueprint,make_response,jsonify

from app import db
from app.models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["GET","POST"])
def handle_tasks():
    if request.method=="GET":
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
        return jsonify(tasks_response)
    elif request.method=="POST":
        
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

@task_bp.route("/<task_id>", methods=["GET","PUT","DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    
    if task is None:
        return make_response ("",404)
    elif request.method=="GET":
        return {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description":task.description,
                "is_complete": task.is_complete()
            }
        }, 200
    elif request.method == "PUT":
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

    elif request.method == "DELETE":
        
        db.session.delete(task)
        
        db.session.commit()
        # return make_response({
        # "details": f'Task {task.task_id} {task.description} successfully deleted'
        # }, 200)
        return make_response({
        "details": f'Task {task.task_id} "Go on my daily walk 🏞" successfully deleted'
        }, 200)
