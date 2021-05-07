from app import db 
from app.models.task import Task
# import the necessary module for our Task model
from flask import request, Blueprint, make_response, Response, jsonify
# import our dependencies. Python supports comma-separated importing.

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
# This is the Blueprint instance. We'll use it to group routes that start with /tasks.
# "tasks" is the debugging name for this Blueprint. __name__ provides information the blueprint uses for certain aspects of routing.
# url_prefix="/tasks" -- A keyword argument. This indicates that every endpoint using this Blueprint should be treated like it starts with /tasks
# ^^ we should use this blueprint for all out RESTful routes that start with /tasks!

# This decortator uses the tasks_bp Blueprint to define an endpoint and accepted HTTP method 
# -- in this case the method is "POST" and the the following function create_task() witll execute whenever a matching HTTP request is recieved.
@tasks_bp.route("", methods=["POST"]) 
def create_task(): # this function will execute when a request matched the decoractor. the function name doesnt affect how requests are routed to this methos. but the function name could include matching the route path - a descriptive Python function name.
    request_body = request.get_json() # the local variable request_body will hold the body contents of the HTTP request in a Python data structre (likely dictionaries, lists, and strings)
    # request.get_json() ^^ use the request object <<imported from flask>> to get information about the HTTP request -- this method .get_json() "Pythonifies the JSON HTTP request body by converting it to a PYthon dictionary.
    new_task = Task(title=request_body["title"], # We can create an instance of Task using the data in request_body. We assign this new instance to the new_task variable
                    description=request_body["description"], #use keyword arguments that match our model attribute, and access the request_body values to create the Task instance
                    completed_at=request_body["completed_at"])
    db.session.add(new_task) # adds the task to the database
    db.session.commit() # saves the task to the database
    #################### I WANT THE RESPONSE TO HAVE "IS_COMPLETE": FALSE ####
    # if new_task[completed_at] == null:
        # new_task[completed_at] = False
    ####################
    # for each endpoint - we must return the HTTP response
    return jsonify(new_task, 201)
    # return make_response(f'Task {new_task.to_json()} successfully created',201)
# make_response() function instantiates a Response object. A Response object is generally what we want to return from Flask endpoint functions.
# .to_json() is a method you must write that belongs to the Task model/class

# return jsonify(new_task) -- ALTERNATIVELY - this was working but missing the 201 response

@tasks_bp.route("", methods=["GET"]) 
def get_all_tasks():
    tasks = Task.query.all()
        # the local vareiable tasks stores the list of Task instances
        # This SQLAlchemy syntax tells Task to query for all() tasks. 
        # ^^ This method returns a list of instances of Task -- that lis is stored in the variable tasks as mentioned ^^
    ##### Test 1.1  -- IF THERE ARE ZERO SAVED TASKS : I WANT A RESPONSE OF 200 OK #####
    tasks_response = [] # set the variable tasks.response as an empty list
    
    for t in tasks: # iterate over the list of all tasks in tasks to collect the data and format it into a response
        each_task = t.to_dictionary()
        tasks_response.append(each_task)
        # tasks_response.append({     # use the tasks_response [] list to hold task dictionaries
        #     "id": task.id,     # this is the format of dictionary we want to send back. We will instert/appendthe values based on the task we're iterating on
        #     "title": task.title,    
        #     "description": task.description,
        #     "is_complete": task.completed_at != None
        # })
    return jsonify(tasks_response)
        # tasks_response contains a list of book dictionaries. 
        # -- To turn it into a Response object, we pass it into jsonify(). This will be our common practice when --
        # -- returning a list of something because the make_response function does not handle lists.


# @tasks_bp.route("", methods=["GET"]) 
# def get_one_task():

    # return make_response()

# @tasks_bp.route("", methods=["PUT"]) 
# def update_tasks():

    # return

# @tasks_bp.route("", methods=["DELETE"]) 
# def delete_tasks():

    # return