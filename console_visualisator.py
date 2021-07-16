from prettytable import PrettyTable

class ConsoleVisualisator:
    def __init__(self):
        self.table = PrettyTable()
        self.table.field_names = ["<< Source >>", "<< Login >>", "<< Password >>"]

    def show(self, notes):
        for note in notes:
            unit = note.get_unit()
            self.table.add_row([unit['source'], unit['login'], unit['password']])
            
        print(self.table)