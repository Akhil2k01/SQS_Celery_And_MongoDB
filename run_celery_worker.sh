#!/bin/sh

echo "Running Concurrent Worker."
. /home/ubuntu/code/venv-server/bin/activate && python3 -m celery -A  sqs_celery_integration.celery worker -l info -f celery_worker.log