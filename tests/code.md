@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def complete_task(task_id):

    task = Task.query.get(task_id)
    complete_task = complete_helper()

    if task == None:
        return make_response("", 404)

    elif task:
        task.completed_at = datetime.datetime.now()
        db.session.commit()
        return ({
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": complete
        }}), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def incomplete_task(task_id):

    task = Task.query.get(task_id)
    complete_task = complete_helper()

    if task == None:
        return make_response("", 404)

    elif task.completed_at == None:
        complete=task.complete_helper()
        db.session.commit()
        return ({
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": complete
        }}), 200
    

# @tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
# def complete_task(task_id):
#     complete_task = complete_helper()
#     if request.method =="PATCH":
#         task = Task.query.get(task_id)
#         complete=task.complete_helper()
#         #update datetime
#         db.session.commit()
#         return ({
#             "task": {
#                 "id": task.id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": complete
#         }}), 200


#PATCH localhost:9000/tasks/1/mark_complete
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):
    
    if request.method == "PATCH":
        
        task = Task.query.get(task_id)
        
        if task is None:
            return jsonify(None), 404
        
        task.completed_at = datetime.now()
        
        return jsonify({"task": task.json_object()}),200