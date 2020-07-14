import pandas as pd
import sqlalchemy


class Database:
    """
        sqlalchemy connection string template:
            dialect+driver://username:password@host:port/database
    """
    def __init__(self, cfg_from_file=True):
        self.cfg_from_file = cfg_from_file
        if cfg_from_file:
            self.db_config = "db-config.csv"

    @property
    def db_config(self):
        return f"Database config from file: {self.cfg_from_file}"

    @db_config.setter
    def db_config(self, file_name):
        config_file = pd.read_csv("./private/"+file_name)
        self._db_config = config_file.to_dict()
        print("self._db_config: ", self._db_config)
