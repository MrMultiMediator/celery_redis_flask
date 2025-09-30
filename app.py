# Run celery like this: celery -A app.celery_app worker --loglevel=info --concurrency=1
from config import create_app #-Line 1

flask_app = create_app()  #-Line 2
celery_app = flask_app.extensions["celery"] #-Line 3

if __name__ == "__main__":
    flask_app.run(debug=True)
