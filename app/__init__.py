from flask import Flask
import concurrent.futures

# Initialize Flask app
app = Flask(__name__)

# Thread pool executor
executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

# Import routes to register them with the app
from app import routes
