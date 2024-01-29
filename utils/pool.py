from utils.pipeline import Pipeline

class Pool:

    def __init__(self):
        self.pipelines = []

    def add_pipeline(self, pipeline: Pipeline):
        self.pipelines.append(pipeline)

    def get_pipeline(self, url, branch):
        for pipeline in self.pipelines:
            if pipeline.url == url and pipeline.branch == branch:
                return pipeline
        return None

    def reset(self):
        self.pipelines = []
