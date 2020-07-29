import pandas as pd
import sqlalchemy
import pymysql


class Database:
    """
        sqlalchemy connection string template:
            dialect+driver://username:password@host:port/database
    """
    def __init__(self, cfg_from_file=True):
        self.cfg_from_file = cfg_from_file
        self.engine = ''
        if cfg_from_file:
            self.db_config = "db-config.csv"
        else:
            self.connect('mysql', 'pymysql', 'user', 'P@$$w0rd', 'localhost', '3306', 'expense_tracker')

    @property
    def db_config(self):
        return f"Database config from file: {self.cfg_from_file}"

    @db_config.setter
    def db_config(self, file_name):
        config_file = pd.read_csv("./private/"+file_name)
        self._db_config = config_file.to_dict()
        print("self._db_config: ", self._db_config)

    def connect(self, dialect, driver, username, password, host, port, database):
        connection_string = '{}+{}://{}:{}@{}:{}/{}'.format(dialect, driver, username, password, host, port, database)
        print('connection_string: ', connection_string)
        self.engine = sqlalchemy.engine.create_engine(connection_string, echo=True)
        print('engine: ', self.engine)
        try:
            self.engine.connect()
        except Exception as e:
            print('DB connection failed: ', e)

    def user_in_db(self, login):
        user_table_df = pd.read_sql('users', self.engine)
        print('user_table_df: ', user_table_df)
