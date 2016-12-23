"""
A script responsible for visualising money expenditure from bank statements.
"""
import numpy as np


def query(entries, keyWord):
    """
    Filters out entries that match the given 'contains' substring in the
    description column.

    :param entries: A dictionary mapping line numbers to transaction entries.
    :param keyWord: The substring that is searched in the description column.
    :return: A dictionary mapping line numbers to transaction entries.
    """
    HEADER = entries[0]
    matches = {0: HEADER}

    for line, entry in entries.items():
        _, _, _, desc = entry

        if desc.find(keyWord) != -1:
            matches[line] = entry

    return matches


def writeData(entries, fPath):
    """
    Writes the given data which contains transaction entries into a text
    file in CSV format.

    :param entries: A dictionary mapping line numbers to transaction entries.
    :param fPath: The path to the output file.
    """
    with open(fPath, "wb") as outF:

        # Writing data using numpy
        entries = [entry for num, entry in entries.items()]
        entries = np.array(entries)
        dFormat = "%10s {0} %9s {0} %8s {0} %s".format(3*" ")
        np.savetxt(outF, np.array(entries), fmt=dFormat)
