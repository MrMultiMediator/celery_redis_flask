from tasks import long_running_task
from celery.result import AsyncResult
from flask import request, jsonify, Blueprint, render_template, current_app

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@views.route("/trigger_task", methods=["POST"])
def start_task() -> dict[str, object]:
    iterations = request.form.get('iterations')
    result = long_running_task.delay(int(iterations))
    # Use the Redis client from the Celery app
    current_app.extensions["celery"].backend.client.lpush("task_ids", result.id)
    return {"result_id": result.id}

@views.route("/get_result", methods=["GET"])
def task_result() -> dict[str, object]:
    result_id = request.args.get('result_id')
    result = AsyncResult(result_id)
    if result.ready():
        if result.successful():
            return {
                "ready": result.ready(),
                "successful": result.successful(),
                "value": result.result,
            }
        else:
            return jsonify({'status': 'ERROR', 'error_message': str(result.result)})
    else:
        return jsonify({'status': 'Running'})

@views.route("/tasks", methods=["GET"])
def get_tasks():
    # Use the Redis client from the Celery app
    task_ids_bytes = current_app.extensions["celery"].backend.client.lrange("task_ids", 0, -1)
    task_ids = [task_id.decode('utf-8') for task_id in task_ids_bytes]
    return jsonify(task_ids)

@views.route("/tasks_list", methods=["GET"])
def tasks_list():
    task_ids_bytes = current_app.extensions["celery"].backend.client.lrange("task_ids", 0, -1)
    task_ids = [task_id.decode('utf-8') for task_id in task_ids_bytes]
    return render_template("tasks.html", task_ids=task_ids)

