from console_visualisator import ConsoleVisualisator
from pass_keeper import Note, PassKeeper

class Assistent:
    def __init__(self):
        self.call_backs_init()

        self.is_auth = False
        self.save_mode = None

        self.notes = []
        self.pass_keeper = None

    def __del__(self):
        if len(self.notes) > 0:
            self.pass_keeper.save(self.notes)

    def check_auth(self):
        if not self.is_auth:
            self.authorisation()

    def authorisation(self):
        db_pass = str(input("\n>> type your db pass: "))
        self.pass_keeper.db_test(db_pass)

    def call_backs_init(self):
        self.modes = ("cmd",
                      "data",
                      "exit")

        self.save_modes = ('db', 'file')

        self.commands = ("print all",
                         "change mode",
                         "exit")

        self.mode_funcs = {'cmd'  : self.cmd_mode,
                           'data' : self.data_mode}

        self.cmd_funcs = {"print all"   : self.print_all}

    def get_save_mode(self):
        mode = None
        for i in range(3):
            m = str(input(">> set save mode (db, file): "))
            if m in self.save_modes: 
                mode = m
                break
            else: 
                print("Error: wrong save mode\n")

        return mode

    def set_save_mode(self):
        mode = self.get_save_mode()
        if mode is not None: 
            self.pass_keeper = PassKeeper(mode)
            self.save_mode = mode
            return True
        else:
            return False

    def data_mode(self):
        if self.save_mode is None:
            if self.set_save_mode():
                print(f"Save mode is accepted: {self.save_mode}")
            else:
                print("Error: save mode is not accepted")
                return

        source   = str(input("\n>> data (source): "))
        login    = str(input(">> data (login): "))
        password = str(input(">> data (password): "))

        self.notes.append(Note(source, login, password))
        print(len(self.notes))

        if len(self.notes) == 3:
            self.pass_keeper.save(self.notes)
            del self.notes[:]

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
