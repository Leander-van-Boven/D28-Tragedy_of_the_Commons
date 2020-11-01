import os,sys

class CsvLogger:
    """Helper class that constructs a CSV table.

    Attributes
    ----------
    head : `list[str]`, 
        The table header, where head[i] is the header for column i.
    
    table : `list[list[str]]`,
        The table, where table[i][j] holds the value of row i, column j.

    n_cols : `int`,
        The amount of columns of this table.

    n_rows : `int`,
        The amount of rows of this table.

    separator : `str`,
        The separator character used in CSV conversion.

    sep_replace : `str`,
        If a table value contains the separator character, 
        it will be replaced by this character.

    Methods
    -------
    `add_row(col_names, sep=',', rep=' ')`
    
    `write(path)`
    """


    def __init__(self, params, col_names, path=None, append=False):
        """Initializes the CsvLogger class.
        
        Parameters
        ----------
        params : `dict`,
            A dictionary containing paramaters for the logger.

        path : `str`, 
            The path to which the output should be written.

        col_names : `list[str]`,
            A list containing the names for each column of the table.
        """

        self.path = path

        self.separator = params['separator']
        self.sep_replace = params['separator_replacement']
        if self.separator == self.sep_replace:
            raise Exception("Separator and its replacement can't be equal!")

        self.head = [col.replace(self.separator, self.sep_replace)
                     for col in col_names]
        self.n_cols = len(col_names)
        self.n_rows = 0
        self.table = list()
        self.append = append


    def add_row(self, row):
        """Adds a row to the table.

        Parameters
        ----------
        row : `list[str]`,
            The row to add, where row[i] will be put at column i.
        """

        if len(row) != self.n_cols:
            raise Exception("Invalid number of columns in row!")
        # self.table.append([str(r).replace(self.separator, self.sep_replace)
        #                    for r in row])
        self.table.append(self.separator.join(
            [str(r).replace(self.separator, self.sep_replace) for r in row])
        )
        self.n_rows += 1


    def write(self, path=None):
        """Writes the table as a CSV file to the specified path.

        Parameters
        ----------
        path : `str`, optional,
            The path to write the file to,
            if not specified self.path is taken.
        """
        if not self.append:
            with open(path or self.path or '.log.csv', 'w') as file:
                file.write(self.separator.join(self.head) + '\n') 
                # file.write('\n'.join([self.separator.join(row) 
                #                       for row in self.table]))
                file.write('\n'.join(self.table))
        else:
            with open(path or self.path or '.log.csv', 'a') as file:
                file.write('\n'.join(self.table))