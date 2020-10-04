#TODO IMPLEMENT!

import os,sys

class CsvLogger:
    def __init__(self, col_names, sep=',', rep=' '):
        if sep == rep:
            raise Exception("rep and sep can't be equal!")
        self.separator = sep
        self.sep_replace = rep
        self._head = sep.join([col.replace(self.separator, self.sep_replace)
                               for col in col_names])
        self.n_cols = len(col_names)
        self.n_rows = 0
        self.rows = list()

    def add_row(self, row):
        if len(row) != self.n_cols:
            raise Exception("Invalid number of columns in row!")
        self.rows.append(self.separator.join(
                            [str(r).replace(self.separator, self.sep_replace)
                             for r in row]))

    def write(self, path):
        with open(path, 'w') as file:
            file.write(self._head + '\n') 
            file.write('\n'.join(self.rows))