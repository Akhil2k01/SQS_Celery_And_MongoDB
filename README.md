# Celery + AWS SQS + MongoDB — Distributed Async Task System

## This project uses celery with AWS SQS message broker to achieve a async processing

Celery is a distributed task queue. It allows you to run time-consuming operations in the background as asynchronous tasks. Celery handles task scheduling, distribution, and execution, making it an essential tool for creating responsive applications.

Amazon SQS is a message queuing service provided by AWS. This service is a fully managed, durable message queuing service that enables decoupling and scaling of microservices, distributed systems, and serverless applications

This repo has a code in which celery and SQS have been integrated to work together, along with the MongoDB is maintain a persistent state maintenance.

What each file has:
1. app.py ---> A flask app which has api endpoint which directs the request to a model
2. config.json ---> configuration file
3. config.py ---> Used to read the config.json file and keep the configuration as an object
4. connection.py ---> Used to connect to MongoDB database.
5. extension.py ---> Has MongoEngine which will be used by the application.
6. middle_layer.py ---> Has the API resource class
7. models.py ---> Has the mongo model used to store the state
8. sqs_celery_integration.py ---> Main file which runs the celery concurrent tasks.
9. mongo_task_state.py ---> Used to insert a initial record to mongo db collection.
10. run_app.sh ---> File used to run the application (Can be made as a microservice, which runs this file)
11. run_celery_scheduler.sh ---> File used to run the Celery Scheduler (Can be made as a microservice, which runs this file)
9. run_celery_worker.sh ---> File used to run the Celery Worker (Can be made as a microservice, which runs this file)
