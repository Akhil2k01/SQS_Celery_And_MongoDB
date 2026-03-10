#!/bin/sh

echo "Running Celery Scheduler."
. /home/ubuntu/code/venv-server/bin/activate && python3 -m celery -A  sqs_celery_integration.celery beat -l info -f celery_scheduler.log
