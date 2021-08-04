import psycopg2 as db
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class Note:
    def __init__(self, source='-', login='-', password='-'):
        self.source = source
        self.login  = login
        self.password = password
        self.unit = {'source' : source, 'login' : login, 'password' : password}

    def get_unit(self):
        return self.unit

    def get_sequence(self):
        return self.source, self.login, self.password

class PassKeeper():
    def selfs_init(self):
        self.modes = ('db', 'file')
        self.db_name   = "passes_db"
        self.file_name = "passes_file.csv"
        self.__db_pass = None

    def __init__(self, mode):
        self.selfs_init()
        if mode not in self.modes:
            raise ValueError('Invalid value for ClassKeeper. Available values - db, file')
        self.mode = mode

        if mode == 'db': self.create_db()

    def __save_in_db(self, notes):
        print("Saved in db")

    def __save_in_file(self, notes):
        print("Saved in file")

    def save(self, notes):
        if self.mode == 'db':
            self.__save_in_db(notes)

        if self.mode == 'file':
            self.__save_in_file(notes)

    def create_db(self):
        try:
            p = str(input("Type db password: "))

            con = db.connect(user = 'postgres', password = p, host = 'localhost', port = '5432')
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE
            cursor = con.cursor()

            cursor.execute("SELECT datname FROM pg_database;")
            db_list = cursor.fetchall()

            if (self.db_name,) not in db_list:
                #Creating a database
                sql = f'''CREATE DATABASE {self.db_name};'''
                cursor.execute(sql)

                #Creating table as per requirement
                sql ='''CREATE TABLE notes(
                        source CHAR(50) NOT NULL,
                        login  CHAR(50) NOT NULL,
                        password CHAR(50) NOT NULL
                        );'''
                cursor.execute(sql)

                print("Database created successfully")
            else:
                print("DB is already exist")

            con.close()

            self.__db_pass = p
        except db.OperationalError:
            print("Error: Wrong password")

    def db_test(self, in_pass):
        try:
            con = db.connect(user = 'postgres', password = in_pass, host = 'localhost', port = '5432')
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE
            cursor = con.cursor()

            #Creating a database
            # sql = '''CREATE DATABASE mydb;'''
            # cursor.execute(sql)
            # print("Database created successfully........")

            cursor.execute("SELECT datname FROM pg_database;")
            db_list = cursor.fetchall()

            print(len(db_list))

            for item in db_list:
                if 'mydb' in item:
                    print("It's here!")
                    print(f"item = {item}, len = {len(item)}")
            
            cursor.execute('select version()')
            data = cursor.fetchone()
            print(f'db version: {data}')

            con.close()

            print('Connection closed')
        except db.OperationalError:
            print("Error: Wrong password")

        

