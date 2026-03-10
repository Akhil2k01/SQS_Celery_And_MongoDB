import json

def read_json_config():
    config_file_path = 'config.json'
    with open(config_file_path) as config_file:
        config = json.load(config_file)
    config_file.close()
    return config

def fetch_config_values():  # called in the config.py file
    """
    Fetching the app configuration values from either param store or config.json
    returns: a dict with all required keys and values
    """

    print("Fetching the config values for the app")
    config = read_json_config()
    print(f"Fetched the config values: {config}")
    return config  # returning dict

class Config(object):
    """
    This class is used to fetch the configuration values for the app
    """

    config = fetch_config_values()
    AWS_REGION = config.get("AWS_REGION", "us-east-1")
    REDBEAT_BROKER_URL = config.get("REDBEAT_SCHEDULER", dict()).get('BROKER_URL', 'redis://localhost:6379/5')
    REDBEAT_RESULT_BACKEND = config.get("REDBEAT_SCHEDULER", dict()).get('RESULT_BACKEND', 'redis://localhost:6379/6')
    REDBEAT_REDIS_URL = config.get("REDBEAT_SCHEDULER", dict()).get('REDBEAT_REDIS_URL', 'redis://localhost:6379/7')

    MONGO_DB_CM_CLOSE_LOOP_ALIAS = config.get('CM_CLOSE_LOOP_MONGO_DB')
    MONGO_URI = "mongodb://{}:{}@{}:{}/".format(config.get("MONGO_USERNAME"),
                                                config.get("MONGO_PWD"),
                                                config.get("MONGO_SERVER"),
                                                config.get("MONGO_PORT"))
    MONGODB_HOST = config.get("MONGO_SERVER")
    MONGODB_PORT = config.get("MONGO_PORT")
    MONGO_USERNAME = config.get('MONGO_USERNAME')
    MONGO_PWD = config.get('MONGO_PWD')
    MONGODB_SETTINGS = [
        {
            'ALIAS': MONGO_DB_CM_CLOSE_LOOP_ALIAS,
            'DB': MONGO_DB_CM_CLOSE_LOOP_ALIAS,
            'HOST': 'mongodb://{}:{}@{}/cm_close_loop_validation'.format(MONGO_USERNAME,
                                                                      MONGO_PWD,
                                                                      MONGODB_HOST),
            'PORT': 27017
        },
    ]