from flask import Flask
from middle_layer import MiddleLayer

from flask_restful import Api
from extension import mongo_db
from config import Config
import logging

app = Flask(__name__)
api = Api(app=app)

app.config.from_object(Config)
mongo_db.init_app(app)
"""
curl -H "Content-Type: application/json" -X POST "http://localhost:3000/start_sqs_task"'
"""
api.add_resource(MiddleLayer, '/start_sqs_task')

if __name__ == "__main__":
    logging.basicConfig(filename='app.log', format='%(asctime)s - %(name)s - \
        %(levelname)s - %(message)s', level=logging.INFO)
    logging.info("hello world...")
    app.run(host="0.0.0.0", port=3000, debug=True)
    