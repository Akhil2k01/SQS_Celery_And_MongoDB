import celery
import random
from config import Config
import logging
from datetime import datetime, timezone
from models import SchedulerEntry
from connection import CmConnection

app = celery.Celery(__name__)

from kombu import Queue

app.conf.task_queues = (
    Queue("test_monitor_queue.fifo"),
    Queue("test_destroy_queue.fifo"),
)

# -------------------------
# SQS Broker Configuration
# -------------------------
app.conf.update(
    broker_url="sqs://",
    result_backend=None,
    broker_transport_options={
        "region": Config.AWS_REGION,
        "visibility_timeout": 3600,
        "polling_interval": 5,
    }
)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Runs every 30 seconds
    sender.add_periodic_task(30.0, monitor_task.s())

    # Runs every 900 seconds (15 minutes)
    sender.add_periodic_task(60.0, destroy_task.s())

def is_task_running(task_name):
    with CmConnection():
        if task_name == "monitor_task":
            records = SchedulerEntry.objects.filter(monitor_task_status="running").only("execution_uuid","cad_topology_job_uuid","monitor_task_status")
            # record = SchedulerEntry.objects.filter(monitor_task_status="running").sort("updated_at").first()
            # SchedulerEntry.objects(_id=record._id).update(set__updated_at=datetime.now(tz=timezone.utc).replace(tzinfo=None))
        elif task_name == "destroy_task":
            records = SchedulerEntry.objects.filter(destroy_task_status="running").only("execution_uuid","cad_topology_job_uuid","monitor_task_status", "destroy_task_status")
            # record = SchedulerEntry.objects.filter(destroy_task_status="running").sort("updated_at").first()
            # SchedulerEntry.objects(_id=record._id).update(set__updated_at=datetime.now(tz=timezone.utc).replace(tzinfo=None))
        else:
            logging.info("Invalid task name provided: %s", task_name)
            return None
    return records

def get_current_utc_time():
    """Helper to get the current UTC time without timezone info."""
    return datetime.now(tz=timezone.utc).replace(tzinfo=None)

def lock_unlock_task(record, task_name, op, now_time):
    """
    Lock a task for processing by updating its status to 'processing'.
    """
    if not record:
        logging.info("Record value is invalid: %s", record)
        return False
    with CmConnection():
        try:
            if op == "lock":
                if task_name == "monitor_task":
                    res = SchedulerEntry.objects(_id=record._id, monitor_task_status="running").update_one(set__monitor_task_status="processing", set__updated_at=now_time)
                elif task_name == "destroy_task":
                    res = SchedulerEntry.objects(_id=record._id, destroy_task_status="running").update_one(set__destroy_task_status="processing", set__updated_at=now_time)
                return res
            elif op == "unlock":
                if task_name == "monitor_task":
                    res = SchedulerEntry.objects(_id=record._id, monitor_task_status="processing").update_one(set__monitor_task_status="running", set__updated_at=now_time)
                elif task_name == "destroy_task":
                    res = SchedulerEntry.objects(_id=record._id, destroy_task_status="processing").update_one(set__destroy_task_status="running", set__updated_at=now_time)
                return res
        except Exception as exc:
            logging.error(f"Error while locking the task: {exc}")
            return False

def deregister_task(record, task_name, now_time):
    """
    deregister a scheduled task.
    """
    if not record:
        logging.info("Record value is invalid: %s", record)
        return False
    with CmConnection():
        try:
            if task_name == "monitor_task":
                res = SchedulerEntry.objects(_id=record._id).update(set__monitor_task_status="completed", set__updated_at=now_time)
            elif task_name == "destroy_task":
                res = SchedulerEntry.objects(_id=record._id).update(set__destroy_task_status="completed", set__updated_at=now_time)
            return res
        except Exception as exc:
            logging.error(f"Error while deregistering the task: {exc}")
            return False

@app.task(bind=True, queue="test_monitor_queue.fifo")
def monitor_task(self):
    records = is_task_running("monitor_task")
    if not records:
        logging.info("No monitor task running. Skipping execution.")
        return "No active monitor tasks"
    for record in records:
        update_res = lock_unlock_task(record, "monitor_task", "lock", get_current_utc_time())
        if update_res != 1:
            logging.warning("Failed to update the monitor task status to processing for execution_uuid: {}".format(record.execution_uuid))
            continue
        logging.info("\n")
        rand_num = random.randint(1, 5)
        logging.info(f"Monitor task _id is {self.request.id} for execution_uuid: {record.execution_uuid} and topology: {record.cad_topology_job_uuid}")
        logging.info("Monitoring task with random number: {}".format(rand_num))

        final_num = rand_num % 2
        logging.info("Final number is {}".format(final_num))
        if final_num == 0:
            logging.info("Final number is 0, deregistering the tmonitor task for execution_uuid: {}".format(record.execution_uuid))
            deregister_task(record, "monitor_task", get_current_utc_time())
            continue
        logging.info(f"Completed monitoring for execution_uuid: {record.execution_uuid} with random number: {rand_num}")
        update_res = lock_unlock_task(record, "monitor_task", "unlock", get_current_utc_time())
        if update_res != 1:
            logging.error("Failed to update the monitor task status to running for execution_uuid: {}".format(record.execution_uuid))
    return True

@app.task(bind=True, queue="test_destroy_queue.fifo")
def destroy_task(self):
    records = is_task_running("destroy_task")
    if not records:
        logging.info("No destroy task running. Skipping execution.")
        return "No active destroy tasks"
    for record in records:
        update_res = lock_unlock_task(record, "destroy_task", "lock", get_current_utc_time())
        if update_res != 1:
            logging.warning("Failed to update the destroy task status to processing for execution_uuid: {}".format(record.execution_uuid))
            continue
        logging.info("\n")
        logging.info(f"Destroy task _id is {self.request.id} for execution_uuid: {record.execution_uuid} and topology: {record.cad_topology_job_uuid}")
        # Check the DB if the monitor task is still running for the same execution_uuid
        if record.monitor_task_status != "completed":
            logging.info("Monitor task is still running for execution_uuid: {}, not deregistering the destroy task".format(record.execution_uuid))
            logging.info("Monitor task is still running for execution_uuid: {}, not deregistering the destroy task".format(record.execution_uuid))
            update_res = lock_unlock_task(record, "destroy_task", "unlock", get_current_utc_time())
            if update_res != 1:
                logging.error("Failed to update the destroy task status to running for execution_uuid: {}".format(record.execution_uuid))
        else:
            logging.info("Monitor task is not running for execution_uuid: {}, deregistering the destroy task".format(record.execution_uuid))
            deregister_task(record, "destroy_task", get_current_utc_time())
            logging.info("Destroy task executed for execution_uuid: {}".format(record.execution_uuid))
    return True


"""
Indexing needed on
monitor_task_status
destroy_task_status
_id, monitor_task_status
_id, destroy_task_status
"""