# Run celery like this: celery -A app.celery_app worker --loglevel=info --concurrency=1
# Spin up all containers like this: docker compose up --build -d
# Then open port 5000 in a browser from the host machine to get the web app
from config import create_app #-Line 1
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Adjust log level as needed
    format="[%(asctime)s]: %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("data/app.log", mode="a"),  # Log to file in append mode
    ],
)

# Get the FileHandler by iterating through handlers
for handler in logging.getLogger().handlers:
    if isinstance(handler, logging.FileHandler):
        file_handler = handler
        break

# Set the log level for the FileHandler
file_handler.setLevel(logging.DEBUG)

flask_app = create_app()  #-Line 2
celery_app = flask_app.extensions["celery"] #-Line 3

if __name__ == "__main__":
    flask_app.run(debug=True)
