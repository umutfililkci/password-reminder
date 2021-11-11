import psycopg2 as db
from psycopg2 import connect, sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import pickle
import csv
import json

import traceback

csv_suffix    = '.csv'
json_suffix   = '.json'
pickle_suffix = '.pickle'

store_pack = 'storage\\'

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
    default_ff   = 'csv'
    default_mode = 'file'

    def selfs_init(self, meta):
        self.update(meta)
        self.__init_callbacks()
        self.modes = ('db', 'file')
        self.db_name   = "passes_db"
        self.__db_pass = None

    def __init_callbacks(self):
        self.save_funcs = {
            'db':   self.__save_in_db,
            'file': self.__save_in_file
        } 
        self.read_funcs = {
            'db':   self.__read_from_db,
            'file': self.__read_from_file
        }

    def __init__(self, meta):
        self.selfs_init(meta)
        if self.mode not in self.modes:
            raise ValueError('Invalid value for ClassKeeper. Available values - db, file')
        # if mode == 'db': self.create_db()'
            
    def update(self, meta):
        self.ff   = meta['file_format']
        self.mode = meta['save_mode']
        if self.ff   == None: self.ff   = PassKeeper.default_ff
        if self.mode == None: self.mode = PassKeeper.default_mode
        self.__set_filename()
         
    def __set_filename(self):
        ff = self.ff
        if   ff == 'csv':    self.file_name = store_pack + 'passes_file' + csv_suffix
        elif ff == 'json':   self.file_name = store_pack + 'passes_file' + json_suffix
        elif ff == 'pickle': self.file_name = store_pack + 'passes_file' + pickle_suffix

    def __save_in_db(self, notes):
        print(f"Is not created for {self.mode} yet. Unsaved!")

    def __write_csv(self, notes):
        with open(self.file_name, 'a', newline='') as f:
            writer = csv.writer(f)
            for note in notes:
                writer.writerow(note.get_sequence())

    def __read_csv(self):
        notes = []
        with open(self.file_name, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                note = Note(*row)
                notes.append(note)

        return notes

    def __save_in_file(self, notes):
        ff = self.ff

        if ff == 'csv': self.__write_csv(notes)
            
        print("Saved in file")

    def save(self, notes):
        self.save_funcs[self.mode](notes)

    def __read_from_db(self):
        # print(f"All is read from {self.ff} file")
        print(f'Is not created for {self.mode} yet! Please change storage')

    def __read_from_file(self):
        ff = self.ff
        notes = None

        if ff == 'csv': notes = self.__read_csv()
            
        print(f"All is read from {self.ff} file\n")
        return notes
    
    def read_all(self):
        return self.read_funcs[self.mode]()

    def create_db(self):
        try:
            p = str(input("Type db password: "))

            con = db.connect(user = 'passes_db', password = p, host = 'localhost', port = '5432')
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE
            cur = con.cursor()

            cur.execute("SELECT datname FROM pg_database;")
            db_list = cur.fetchall()

            if (self.db_name,) not in db_list:
                #Creating a database
                sql = f'''CREATE DATABASE {self.db_name};'''
                cur.execute(sql)

                # cur.close()
                # con.close()
                sql = f''' \c {self.db_name} ;'''
                cur.execute(sql)

                # con = db.connect(user = self.db_name, password = p, host = 'localhost', port = '5432')
                
                # cur = con.cursor()

                #Creating table as per requirement
                sql ='''CREATE TABLE notes(
                        source CHAR(50) NOT NULL,
                        login  CHAR(50) NOT NULL,
                        password CHAR(50) NOT NULL
                        );'''
                cur.execute(sql)

                print("Database created successfully")
            else:
                print("DB is already exist")


            cur.close()
            con.close()

            self.__db_pass = p
        except Exception as ex:
            print(ex.__class__.__name__)
            traceback.print_exc()
        # except db.OperationalError:
        #     print("Error: Wrong password")

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

        

