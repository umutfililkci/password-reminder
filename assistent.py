from console_visualisator import ConsoleVisualisator

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

class Assistent:
    def __init__(self):
        self.modes = ("cmd",
                      "data",
                      "exit")

        self.commands = ("print all",
                         "change mode",
                         "exit")

        self.mode_funcs = {'cmd'  : self.cmd_mode,
                           'data' : self.data_mode}

        self.cmd_funcs = {"print all"   : self.print_all}

        self.notes = []

    def data_mode(self):
        source = str(input("\n>> data (source): "))
        login = str(input(">> data (login): "))
        password = str(input(">> data (password): "))

        self.notes.append(Note(source, login, password))
        print(len(self.notes))

    def print_all(self):
        con_vis = ConsoleVisualisator()
        con_vis.show(self.notes)

    def cmd_request(self):
        cmd = str(input("\n>> cmd: "))
        return cmd

    def cmd_mode(self):
        commands = self.commands
        cmd_funcs = self.cmd_funcs

        cmd = str(input(">> cmd: "))
        while cmd != 'exit' and cmd != 'change mode':
            if cmd in commands:
                cmd_funcs[cmd]()
            else:
                print("Error: invalid comand")
                print(f"Available cammands list: {commands}")
        
            cmd = self.cmd_request()

    def mode_request(self):
        mode = str(input("\nWhat mode do you wish, sir? : "))
        return mode

    def run(self):
        modes = self.modes
        mode_funcs = self.mode_funcs

        mode = self.mode_request()
        while mode != 'exit':
            if mode in modes:
                mode_funcs[mode]()
            else:
                print("Error: invalid mode...")
                print(f"Available modes list: {modes}\n")

            mode = self.mode_request()

        print("Session is ended. Goodbye, sir!")
