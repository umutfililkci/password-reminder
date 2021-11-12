from console_visualisator import ConsoleVisualisator
from pass_keeper import Note, PassKeeper

import os

class Assistent:
    def __init__(self):
        self.call_backs_init()

        self.is_auth = False

        self.notes = []
        self.pass_keeper = PassKeeper(self.meta)

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

        self.save_modes   = ('db', 'file')

        self.file_formats = ('pickle', 'csv', 'json')

        self.commands = ("print all",
                         "print meta",
                         "change mode",
                         "set file format",
                         "change storage",
                         "cls",
                         "exit")

        self.meta = {
            'save_mode' : None,
            'file_format': None
        }

        self.mode_funcs = {'cmd'  : self.cmd_mode,
                           'data' : self.data_mode}

        self.cmd_funcs = {"print all"      : self.print_all,
                          "print meta"     : self.print_meta,
                          "set file format": self.set_file_format,
                          "change storage" : self.change_storage,
                          "cls"            : self.clear_console
                          }

    def change_storage(self):
        self.set_save_mode()

    def clear_console(self):
        os.system('cls')

    def print_meta(self):
        meta = self.meta
        print(  f"current save mode is << {meta['save_mode']} >>")
        print(f"current file format is << {meta['file_format']} >>")
        
    def get_save_mode(self):
        mode = None
        for i in range(3):
            m = str(input(f">> set save mode {self.save_modes}: "))
            if m in self.save_modes: 
                mode = m
                break
            else: 
                print("Error: wrong save mode\n")

        return mode

    def get_file_format(self):
        ff = None
        ffs = self.file_formats
        for i in range(3):
            f = str(input(f">> set file format {ffs}: "))
            if f in ffs: 
                ff = f
                break
            else: 
                print("Error: wrong file format\n")

        return ff

    def set_save_mode(self):
        mode = self.get_save_mode()
        if mode is not None: 
            self.meta['save_mode'] = mode
            self.pass_keeper.update(self.meta)
            print(f"Save mode is accepted: {mode}")
            return True
        else:
            print("Error: save mode is not accepted")
            return False

    def set_file_format(self):
        ff = self.get_file_format()
        if ff is not None: 
            self.meta['file_format'] = ff
            self.pass_keeper.update(self.meta)
        else:
            print("Error: file format is not accepted")

    def data_mode(self):
        if not self.set_save_mode(): return

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
        notes = self.pass_keeper.read_all()
        if notes is None: notes =  self.notes
        else:             notes += self.notes
        con_vis.show(notes)

    def cmd_request(self):
        cmd = str(input("\n>> cmd: "))
        return cmd

    def cmd_mode(self):
        commands = self.commands
        cmd_funcs = self.cmd_funcs

        cmd = self.guess_cmd_abr(self.cmd_request()) 
        while cmd != 'exit' and cmd != 'change mode':
            if cmd in commands:
                cmd_funcs[cmd]()
            else:
                print("Error: invalid comand")
                print(f"Available cammands list: {commands}")
        
            cmd = self.guess_cmd_abr(self.cmd_request())
            # cmd = self.cmd_request()

    def mode_request(self):
        mode = str(input("\nWhat mode do you wish, sir? : "))
        return mode

    def run(self):
        modes = self.modes
        mode_funcs = self.mode_funcs

        mode = self.guess_cmd_abr(self.mode_request())
        while mode != 'exit':
            if mode in modes:
                mode_funcs[mode]()
            else:
                print("Error: invalid mode...")
                print(f"Available modes list: {modes}\n")

            mode = self.guess_cmd_abr(self.mode_request())

        print("Session is ended. Goodbye, sir!")

    def guess_cmd_abr(self, guess):
        for val in self.commands:
            words = val.split(' ')
            gl = len(guess)
            if gl == len(words):
                mc = 0 # match count
                for i in range(gl):
                    if guess[i] == words[i][0]: mc += 1
                if mc == gl: return val

        return guess
                
