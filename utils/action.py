from utils.constants import *
import os

class Action:

    def __init__(self, pipeline, name, command, command_type):
        self.pipeline = pipeline
        self.name = name
        self.command = command
        self.command_type = command_type
        self.options = dict()
        self.options['connection'] = None
        self.options['user'] = None
        self.options['password'] = None
        self.options['host'] = None
        self.options['database'] = None
        self.options['schema'] = None
        self.options['directory'] = None
        self.options['file'] = None

        self.validate_action()

    def set_database_connection(self, username, password, host, database, schema, connection):
        self.options['connection'] = connection
        self.options['user'] = username
        self.options['password'] = password
        self.options['host'] = host
        self.options['database'] = database
        self.options['schema'] = schema

    def __str__(self):
        return self.name + ": " + self.command

    def validate_action(self):
        command_splitted = self.command.split(' ')
        if self.command_type == COMMAND_COPY:
            if len(command_splitted) > 2:
                 # Error en el comando
                return
            if not os.path.isdir(command_splitted[1]):
                # No existe el directorio
                return
            self.options['directory'] = command_splitted[1]
        if self.command_type == COMMAND_RUN:
            if len(command_splitted) > 2:
                 # Error en el comando
                return
            if not os.path.isfile(command_splitted[1]):
                # No existe el directorio
                return
            self.options['file'] = command_splitted[1]
