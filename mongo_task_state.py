from models import SchedulerEntry

import uuid
from datetime import datetime, timezone

class TaskHelper(object):
    @staticmethod
    def insert_into_scheduler_entry(topology_uuid, username, model_name, execution_uuid, is_prod_execution):
        """
        Inserts a new entry into the SchedulerEntry collection.
        """
        try:
            scheduler_record = SchedulerEntry(
                _id = execution_uuid,
                execution_uuid = execution_uuid,
                model_name = model_name,
                cad_topology_job_uuid = topology_uuid,
                is_prod_execution = is_prod_execution,
                username = username,
                updated_at = datetime.now(tz=timezone.utc).replace(tzinfo=None),
                created_at = datetime.now(tz=timezone.utc).replace(tzinfo=None)
            )
            _ = scheduler_record.save()
            print(f"Inserted entry in SchedulerEntry with topology: {topology_uuid} and execution_uuid: {execution_uuid}")
        except Exception as e:
            print(f"Error inserting entry: {e}")

    @classmethod
    def store_mongo_task_state(cls, topology_uuid, username, model_name, execution_uuid, is_prod_execution):
        """
        Stores task state data for execution.
        """
        execution_uuid = str(uuid.uuid4())  
        TopologyHelper.insert_into_scheduler_entry(topology_uuid, username, model_name, execution_uuid, is_prod_execution)
        return True
        
