import psycopg2 as db

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
    def __init__(self, mode):
        self.modes = ('db', 'file')

        if mode not in self.modes:
            raise ValueError('Invalid value for ClassKeeper. Available values - db, file')

        self.mode = mode

    def __save_in_db(self, notes):
        print("Saved in db")

    def __save_in_file(self, notes):
        print("Saved in file")

    def save(self, notes):
        if self.mode == 'db':
            self.__save_in_db(notes)

        if self.mode == 'file':
            self.__save_in_file(notes)

    def db_test(self, in_pass):
        try:
            conn = db.connect(user = 'postgres', password = in_pass, host = 'localhost', port = '5432')

            cursor = conn.cursor()

            sql = '''CREATE database mydb;'''

            #Creating a database
            cursor.execute(sql)
            print("Database created successfully........")

            # list_database = cursor.fetchall()
            # print(list_database)

            cursor.execute('select version()')
            data = cursor.fetchone()
            print(f'db version: {data}')

            conn.close()

            print('Connection closed')
        except db.OperationalError:
            print("Error: Wrong password")

        

