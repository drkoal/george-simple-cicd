import subprocess

from utils.action import Action
from utils.constants import *
from git import Repo
import os
from os import path
import shutil
import stat
from subprocess import Popen
from utils.connection import ConnectionFactory, Connection

class Executer:

    def __init__(self, action:Action):
        self.action = action
        pass

    def run(self):
        if self.action.command_type == COMMAND_RUN:
            self.command_run()
        if self.action.command_type == COMMAND_COPY:
            self.command_copy()
        if self.action.command_type == COMMAND_SQL:
            self.command_sql()

    def command_run(self):
        p = Popen(self.action.options['file'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        self.action.pipeline.process.append(p)

    def command_copy(self):
        url = self.action.pipeline.url
        directory = self.action.options['directory']
        for root, dirs, files in os.walk(directory):
            for dir in dirs:
                os.chmod(path.join(root, dir), stat.S_IRWXU)
            for file in files:
                os.chmod(path.join(root, file), stat.S_IRWXU)
        shutil.rmtree(directory)
        r = Repo.clone_from(url, directory, branch=self.action.pipeline.branch)
        r.close()

    def command_sql(self):
        connection = ConnectionFactory().get_connection(self.action.options['connection'])
        result = connection.setup_connection(self.action.options)
        directory = self.action.command.split(' ')[1]
        for root, dirs, files in os.walk(directory):
            for file in files:
                if '.sql' not in file: continue
                file_content = open(os.path.join(directory, file), 'r')
                all_lines = file_content.read()
                connection.execute(all_lines)
                connection.commit()

