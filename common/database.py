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
        self.tables = {}
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
        """
        Check if user in 'users' db table
        :param login:
        :return: True if user in db.table.users else False
        """
        _user_registered = False
        _user_password = ''
        if not self.engine.has_table(self.engine, 'users'):
            self.table_user_create()
            return _user_registered, [], _user_password
        user_table_df = pd.read_sql('users', self.engine)
        self.tables['users'] = user_table_df
        print('user_table_df: ', user_table_df)
        _user_registered = login in user_table_df['nickname'].values.tolist()
        return _user_registered, user_table_df['nickname'].values.tolist(), _user_password

    def user_data_load(self, login):
        user_data = {}
        try:
            user_table_df = self.tables.get('users', pd.read_sql('users', self.engine))
            user_data = user_table_df.loc[login].to_dict()
            print('user_data: ', user_data)
        except Exception as e:
            user_data['error'] = e
            print('Failed loading user data: ', e)
        return user_data

    def register_new_user(self, login, password_obj, first_name, last_name, email, last_login_date):
        user_data = {}
        try:
            df = pd.DataFrame({
                'nickname': login,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password_obj.get_password(),
                'last_login_date': last_login_date
            })
            print('df: ', df)
            df.to_sql('users', con=self.engine, index_label='id')
        except Exception as e:
            user_data['error'] = e
            print('Failed registering new user: ', e)

        self.tables_update(table_name='users')
        try:
            user_data = self.tables['users'].loc[login].to_dict()
        except Exception as e:
            user_data['error'] = e
            print('Failed loading user data: ', e)
        return user_data

    # db tables methods
    def tables_update(self, table_name=None):
        return self

    def table_user_create(self):
        """
        Creates 'users' table
        :return: self
        """
        metadata = sqlalchemy.MetaData(self.engine)
        sqlalchemy.Table('users', metadata,
                         sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, nullable=False, autoincrement=True),
                         sqlalchemy.Column('nickname', sqlalchemy.String, nullable=False),
                         sqlalchemy.Column('first_name', sqlalchemy.String, nullable=True),
                         sqlalchemy.Column('last_name', sqlalchemy.String, nullable=True),
                         sqlalchemy.Column('email', sqlalchemy.String, nullable=True),
                         sqlalchemy.Column('password', sqlalchemy.String, nullable=False),
                         sqlalchemy.Column('last_login_date', sqlalchemy.DateTime, nullable=False)
                         )
        metadata.create_all()
        return self
