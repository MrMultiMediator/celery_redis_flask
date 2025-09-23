from tasks import flask_app, long_running_task #-Line 1
from celery.result import AsyncResult#-Line 2
from flask import request,jsonify 

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
    #if request.method == "POST":

    return render_template("home.html")

@views.route("/trigger_task", methods=["POST"])
def start_task() -> dict[str, object]:
    iterations = request.args.get('iterations')
    print(iterations)
    result = long_running_task.delay(int(iterations))#-Line 3
    return {"result_id": result.id}

@views.route("/get_result", methods=["GET"])
def task_result() -> dict[str, object]:
    result_id = request.args.get('result_id')
    result = AsyncResult(result_id)#-Line 4
    if result.ready():#-Line 5
        # Task has completed
        if result.successful():#-Line 6
    
            return {
                "ready": result.ready(),
                "successful": result.successful(),
                "value": result.result,#-Line 7
            }
        else:
        # Task completed with an error
            return jsonify({'status': 'ERROR', 'error_message': str(result.result)})
    else:
        # Task is still pending
        return jsonify({'status': 'Running'})

