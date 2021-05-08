from app import db 
from .models.task import Task
# import the necessary module for our Task model
from flask import request, Blueprint, make_response, Response, jsonify
# import our dependencies. Python supports comma-separated importing.

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
# This is the Blueprint instance. We'll use it to group routes that start with /tasks.
# "tasks" is the debugging name for this Blueprint. __name__ provides information the blueprint uses for certain aspects of routing.
# url_prefix="/tasks" -- A keyword argument. This indicates that every endpoint using this Blueprint should be treated like it starts with /tasks
# ^^ we should use this blueprint for all out RESTful routes that start with /tasks!

# This decortator uses the tasks_bp Blueprint to define an endpoint and accepted HTTP method 
# -- in this case the method is "POST" and the the following function create_task() will execute whenever a matching HTTP request is recieved.
@tasks_bp.route("", methods=["POST"]) # The route usually starts with the model plural - but the tasks_bp Blueprint - is already providing the url_prefix="/books"
def create_task(): # this function will execute when a request matched the decoractor. the function name doesnt affect how requests are routed to this method.
    request_body = request.get_json() # the local variable request_body will hold the body contents of the HTTP request in a Python data structre (likely dictionaries, lists, and strings)
    # request.get_json() ^^ use the request object <<imported from flask>> to get information about the HTTP request - the method .get_json() grabs the part of the HTTP request_body that's in JSON format
    new_task = Task(title=request_body["title"], # We can create an instance of Task using the data in request_body. We assign this new instance to the new_task variable
                    description=request_body["description"], #use keyword arguments that match our model attribute, and access the request_body values to create the Task instance
                    completed_at=request_body["completed_at"])
    db.session.add(new_task) # adds the task to the database
    db.session.commit() # saves the task to the database

    # for each endpoint - we must return the HTTP response
    return jsonify(new_task), 201

# make_response() function instantiates a Response object. A Response object is generally what we want to return from Flask endpoint functions.

@tasks_bp.route("", methods=["GET"]) 
def get_all_tasks():
    tasks = Task.query.all()
        # the local vareiable tasks stores the list of Task instances
        # This SQLAlchemy syntax tells Task to query for all() tasks. 
        # ^^ This method returns a list of instances of Task -- that lis is stored in the variable tasks as mentioned ^^
    ##### Test 1.1  PASSED ###
    tasks_response = [] # set the variable tasks.response as an empty list    
    for t in tasks: # iterate over the list of all tasks in tasks to collect the data and format it into a response
        each_task = t.to_dictionary()
        tasks_response.append(each_task)
        # tasks_response.append({     # use the tasks_response [] list to hold task dictionaries
        #     "id": task.id,     # this is the format of dictionary we want to send back. We will insert/append the values based on the task we're iterating on
        #     "title": task.title,    
        #     "description": task.description,
        #     "is_complete": task.completed_at != None
        # })
    return jsonify(tasks_response), 200
        # tasks_response contains a list of book dictionaries. 
        # -- To turn it into a Response object, we pass it into jsonify(). This will be our common practice when --
        # -- returning a list of something because the make_response function does not handle lists.


# Getting a task by it's ID number
@tasks_bp.route("/<task_id>", methods=["GET"]) 
# ^^ The <task_id> placeholder shows that we're looking for a variable value (could be 1, 2, or 3000). 
# ^^ We'll use this value in the function as the variable task_id, so we should use a good, descriptive name

# The get_task(task_id) function, below, is called whenever the HTTP request matches the decorator. 
# We must add a parameter to this function (task_id). This parameter name must match the route parameter in the decorator. 
# It will receive the part of the request path that lines up with the placeholder in the route.
def get_task(task_id):
    task = Task.query.get(task_id) 
            # ^ This is the SQLAlchemy syntax to query for one Task resource. This method returns an instance of Task.
            # ^ We must pass in the primary key of a task here. The primary key of the task we're looking for was provided in the route parameter, task_id.
    if task:
        response = {
            "id": task.id,
            "title": task.title,
            "description": task.description
        }
        return jsonify(task=task.to_dictionary()), 200
    else:
        response = None
        return jsonify(response), 404


# @tasks_bp.route("", methods=["PUT"]) 
# def update_tasks():

    # return



# @tasks_bp.route("", methods=["DELETE"]) 
# def delete_tasks():

    # return