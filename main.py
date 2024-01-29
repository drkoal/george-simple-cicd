from flask import Flask, request, Response
from utils.pool import Pool
from utils.utils import load_pipelines, create_new_pipeline
from utils.executer import Executer
from utils.constants import *
from utils.configuration import Configuration
from utils.log import Log
from subprocess import Popen

app = Flask(__name__)
pool = Pool()
configuration = Configuration()
log = Log()


@app.route("/", methods=['POST'])
def webhook():
    log.log("REQUEST", "New request [ gitlab ]")
    webhook_info = request.json
    event = webhook_info['event_name']
    if event != EVENT_GIT_PUSH: return Response(status=500)
    branch = webhook_info['ref'].split('/')[2]
    url = webhook_info['repository']['homepage']
    pipeline = pool.get_pipeline(url, branch)
    if pipeline is not None:
        log.log("RUN", "Run pipeline [" + pipeline.name + "] for ["+pipeline.url + "]")
        for x in pipeline.process: Popen("TASKKILL /F /PID {} /T".format(x.pid))
        for action in pipeline.actions:
            log.log("RUN", "Run action [" + action.name + "] for [" + pipeline.url + "]")
            executer = Executer(action)
            executer.run()
    return Response(status=200)


@app.route("/new_pipeline", methods=['POST'])
def new_pipeline():
    log.log("REQUEST", "New request [ new_pipeline ]")
    new_pipeline_info = request.json
    create_new_pipeline(new_pipeline_info)
    pool.reset()
    for pipeline in load_pipelines():
        pool.add_pipeline(pipeline)
    return Response(status=200)


@app.route("/get_pipelines", methods=['GET'])
def get_pipelines():
    log.log("REQUEST", "New request [ get_pipelines ]")

    all_pipelines = []
    for pipeline in pool.pipelines:
        all_pipelines.append(pipeline.__dict__())
    return all_pipelines


if __name__ == "__main__":
    log.log("INIT", "**************************************************")
    log.log("INIT", "Initiating server instance")
    for pipeline in load_pipelines():
        pool.add_pipeline(pipeline)
        log.log("LOAD PIPELINE", "Pipeline loaded [" + pipeline.name + "]")
    log.log("INIT", "Server ready to receive requests")
    app.run(host=configuration.config['host-ip'], port=configuration.config['host-port'])