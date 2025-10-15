import os
from celery import Celery, Task
from flask import Flask

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def create_app() -> Flask:
    app = Flask(__name__)

    from views import views
    app.register_blueprint(views, url_prefix='/')


    # In config.py, I added task_acks_late=True and
    # worker_prefetch_multiplier=1 to the Celery
    # settings. This tells a worker to only grab one task at a time and
    # not to ackowledge it until it's finished
    app.config.from_mapping(
        CELERY=dict(
            broker_url=os.environ.get('CELERY_BROKER_URL', 'redis://localhost'),
            result_backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost'),
            task_ignore_result=False,
            task_list_max_size=4,
            task_acks_late=True,
            worker_prefetch_multiplier=1,
        ),
    )   
    app.config.from_prefixed_env()
    app.jinja_env.auto_reload = True
    celery_init_app(app)
    return app 

