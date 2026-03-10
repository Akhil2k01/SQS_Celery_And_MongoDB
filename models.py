import json
import logging
# import os.path
import secrets
from datetime import datetime

from config import Config
from extension import mongo_db

class SchedulerEntry(mongo_db.Document):
    meta = {
        'db_alias': Config.MONGO_DB_CM_CLOSE_LOOP_ALIAS,
        'collection': 'cm_scheduler_entry'
    }
    _id = mongo_db.StringField(primary_key=True)
    execution_uuid=mongo_db.StringField()
    model_name = mongo_db.StringField()
    cad_topology_job_uuid = mongo_db.StringField()
    is_prod_execution = mongo_db.StringField(default="false")
    username = mongo_db.StringField()
    monitor_task_status = mongo_db.StringField(default="running")
    destroy_task_status = mongo_db.StringField(default="running")
    updated_at = mongo_db.DateTimeField()
    updated_by = mongo_db.StringField(default="application")
    created_at = mongo_db.DateTimeField()