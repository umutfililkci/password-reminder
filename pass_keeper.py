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

    def save_in_db(self, note):
        pass

    def save_in_file(self, note):
        pass

    def save(self, note):
        if self.mode == 'db':
            self.save_in_db(note)

        if self.mode == 'file':
            self.save_in_file(note)

    def db_test(self):
        conn = db.connect(database = 'postgres', user = 'postgres', password = 'vthctltc50', host = 'localhost')

        cursor = conn.cursor()

        cursor.execute('select version()')
        data = cursor.fetchone()
        print(f'db version: {data}')

        conn.close()

        print('Connection closed')

