from app import db
from flask import Blueprint
from .models.task import Task
from flask import request
from flask import jsonify 

# creating instance of the class, first arg is name of app's module
task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#create a task with null completed at
@task_bp.route("", methods = ["POST"], strict_slashes = False)
def create_task():

    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
            description=request_body["description"],
            completed_at = request_body["completed_at"])

    db.session.add(new_task) # "adds model to the db"
    db.session.commit() # does the action above
    return new_task.to_json_response(), 201
    
#     jsonify({"success": True,
#             "message": f"Planet {new_planet.title} has been created"
#             }), 201
# {
#             "id": planet.id,
#             "title": planet.title,
#             "description": planet.description,
#             "radius": planet.radius,
#         }
# if request_body == None or request_body.get("title") == None \
#     or request_body.get("description") == None\
#         or request_body.get("completed_at") == None:
#     return {"details": "Invalid data"}, 404
# elif request_body and request_body.get("title") != None \
#     and request_body.get("description") != None\
#         and request_body.get("completed_at") == null:
#     return {

#     to_dict(request_body)
#     {"task": {"id": 1,
#                     "title": "A Brand New Task",
#                     "description": "Test Description",
#                     "is_complete": false}
# }, 404

