import os,sys

class CsvLogger:
    """Helper class that constructs a CSV table

    Attributes
    ----------
    head : `list[str]`
        the table header, where head[i] is the header for column i
    
    table : `list[list[str]]`
        the table, where table[i][j] holds the value of row i, column j

    n_cols : `int`
        the amount of columns of this table

    n_rows : `int`
        the amount of rows of this table

    separator : `str`
        the separator character used in CSV conversion

    sep_replace : `str`
        if a table value contains the separator character, it will be 
        replaced by this character

    Methods
    -------
    `add_row(col_names, sep=',', rep=' ')`
    
    `write(path)`
    """
    def __init__(self, col_names, sep=',', rep=' '):
        '''Initializes the CsvLogger class.
        
        Parameters
        ----------
        col_names : `list[str]`
            The table header 

        sep : `str`
            The separator character

        rep : `str`
            The replacement character for the separator in table values
        '''
        if sep == rep:
            raise Exception("rep and sep can't be equal!")
        self.separator = sep
        self.sep_replace = rep
        self.head = [col.replace(self.separator, self.sep_replace)
                     for col in col_names]
        self.n_cols = len(col_names)
        self.n_rows = 0
        self.table = list()

    def add_row(self, row):
        '''Adds a row to the table.

        Parameters
        ----------
        row : `list[str]`
            The row to add, where row[i] will be put at column i
        '''
        if len(row) != self.n_cols:
            raise Exception("Invalid number of columns in row!")
        self.table.append([str(r).replace(self.separator, self.sep_replace)
                           for r in row])
        self.n_rows += 1

    def write(self, path):
        '''Writes the table as a CSV file to the specified path.

        Parameters
        ----------
        path : `str`
            The path to write the file to
        '''
        with open(path, 'w') as file:
            file.write(self.separator.join(self.head) + '\n') 
            file.write('\n'.join([self.separator.join(row) 
                                  for row in self.table]))