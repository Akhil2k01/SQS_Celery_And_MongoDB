import logging
from flask_restful import Resource
from mongo_task_state import TaskHelper

class MiddleLayer(Resource):
    def post(self):
        try:
            res = TaskHelper.store_mongo_task_state(topology_uuid="123", username="test_user", model_name="test_model", execution_uuid="", is_prod_execution="false")
            print(f"Response from split_and_store_topology_cm: {res}")
            return {'message': 'Scheduled an execution for the redis: {}'.format("123"),'statusCode': 200}
        except Exception as err:
            logging.error(f"ERROR: {err}")
            return {'message': str(err),'statusCode': 400}, 400
