import os
import sys
import yaml
from utils.action import Action
from utils.pipeline import Pipeline
from utils.constants import *
from utils.log import Log

def load_pipelines():
    log = Log()
    pipelines = []
    all_pipelines = os.listdir("pipelines")
    log.log("LOAD", "Starting to load all the pipelines")
    for file in all_pipelines:
        file_content = open(os.path.join('pipelines',file), 'r')
        log.log("LOAD", "Loading new pipeline [" + file + "]")
        pipeline_yml = yaml.safe_load(file_content)
        new_pipeline = Pipeline(pipeline_yml['name'], pipeline_yml['url'], pipeline_yml['branch'])
        for action in pipeline_yml['actions']:
            command_type = action['command'].split(' ')[0]
            if command_type not in [COMMAND_RUN, COMMAND_COPY, COMMAND_SQL]:
                #ERROR Loading the pipeline
                continue
            new_action = Action(new_pipeline, action['name'], action['command'], command_type)
            user = None
            password = None
            host = None
            connection = None
            database = None
            schema = None
            if 'options' in action:
                if 'user' in action['options']: user = action['options']['user']
                if 'password' in action['options']: password = action['options']['password']
                if 'host' in action['options']: host = action['options']['host']
                if 'connection' in action['options']: connection = action['options']['connection']
                if 'database' in action['options']: database = action['options']['database']
                if 'schema' in action['options']: schema = action['options']['schema']
                new_action.set_database_connection(user, password, host, database, schema, connection)
            new_pipeline.add_action(new_action)
        pipelines.append(new_pipeline)
    log.log("LOAD", "Finished to load all the pipelines")
    return pipelines

def stop_execution():
    sys.exit()

def create_new_pipeline(post):
    log = Log()
    with open(os.path.join('pipelines',post['name'].replace(' ', '_')+'.yml'), 'w') as outfile:
        yaml.dump(post, outfile, sort_keys=False)
        log.log("CREATE", "Create new pipeline file")