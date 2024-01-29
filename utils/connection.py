from abc import ABC, abstractmethod
import sqlite3
import mysql.connector
from utils.constants import *
import psycopg2


class Connection(ABC):

    def __init__(self):
        self.conn = None
        self.is_executing = False
        self.database = None
        self.schema = None

    def setup_connection(self, configuration: dict):
        try:
            self.get_connection(configuration)
            if self.conn is None: return False
            self._get_cursor()
            return True
        except Exception as e:
            return False

    @abstractmethod
    def get_connection(self, configuration: dict):
        pass

    def _get_cursor(self):
        if self.conn is None:
            self.cursor = None
        else:
            self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        try:
            self.conn.close()
        except:
            pass

    def execute(self, all_queries: str):
        """Return a boolean with the result of the execution."""
        self.is_executing = True
        if self.cursor is None:
            self.is_executing = False
            return False


        if len(all_queries) == 0:
            return True
        queries = all_queries.split(";")
        num_queries = len(queries)
        if queries[-1] == "": num_queries -= 1

        num_queries_executed = 0
        for q in queries:
            if q is None or q.strip() == '':
                continue
            try:
                q = q.strip()
                self.cursor.execute(q)
                num_queries_executed += 1
            except Exception as e:
                self.is_executing = False
                return False
            #if(self.connection_type == CONNECTION_FIREBIRD): self.connection.commit()
        self.is_executing = False
        return True

    def get_query_result(self):
        return self.cursor.fetchall()


class ConnectionSQLite(Connection):

    def get_connection(self, configuration: dict):

        self.database = 'MAIN'
        self.schema = None

        self.conn = sqlite3.connect(configuration['host'])
        sqlite3.enable_callback_tracebacks(True)


class ConnectionMySQL(Connection):

    def get_connection(self, configuration: dict):

        self.conn = mysql.connector.connect(
            user = configuration['user'],
            password = configuration['password'],
            host = configuration['host'],
            database = configuration['database']
        )


class ConnectionPostgreSQL(Connection):

    def get_connection(self, configuration: dict):

        self.conn = psycopg2.connect(
            user = configuration['user'],
            password = configuration['password'],
            host = configuration['host'],
            database = configuration['database'],
            options= '-c search_path='+configuration['schema']
        )


#####################################################################################

class ConnectionFactory:
    def get_connection(self, name_connection: str):
        if name_connection.upper() == CONNECTION_SQLITE.upper():
            return ConnectionSQLite()
        elif name_connection.upper() == CONNECTION_MYSQL.upper():
            return ConnectionMySQL()
        elif name_connection.upper() == CONNECTION_POSTGRESQL.upper():
            return ConnectionPostgreSQL()
        else:
            return None

