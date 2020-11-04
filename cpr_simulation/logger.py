import os
import sys
from .exception import InvalidParameterError


class CsvLogger:
    """Helper class that constructs a CSV file.

    Refer to the documentation
    > https://leander-van-boven.github.io/D28-Tragedy_of_the_Commons/
        pages/architecture/#csv-logger
    for a brief explanation of this class.
    And to
    > https://leander-van-boven.github.io/D28-Tragedy_of_the_Commons/
        pages/output/#csv-logger
    for a thorough explanation of the output.
    """

    def __init__(self, params, col_names, path=None, append=False):
        """Initializes the CsvLogger class.

        Parameters
        ----------
        params : `dict`,
            A dictionary containing parameters for the logger.

        col_names : `list[str]`,
            A list containing the names for each column of the table.

        path : `str`,
            The path to which the output should be written.

        append : `bool`,
            Whether to append this table to the file (assumes path is a
            file that already exists). Will not copy over this table's
            header row.
        """

        self.path = path
        self.separator = params['separator']
        self.sep_replace = params['separator_replacement']
        if self.separator == self.sep_replace:
            raise InvalidParameterError(
                "CSV separator and its replacement can't be equal!")

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
        row : `list[obj]`,
            The row to add, where row[i] will be put at column i.
        """

        if len(row) != self.n_cols:
            raise Exception("Invalid number of columns in row!")
        self.table.append(self.separator.join(
            [str(r).replace(self.separator, self.sep_replace) for r in row]))
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
                file.write('\n'.join(self.table))
        else:
            with open(path or self.path or '.log.csv', 'a') as file:
                file.write('\n'.join(self.table))
