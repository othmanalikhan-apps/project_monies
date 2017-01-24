"""
A script responsible for parsing bank statement files from Santander.

The files are text files with ISO-8859-1 encoding written in a specific format.
"""
import pandas as pd


def readFile(fPath):
    """
    Reads the Santander text file which is a bank statement file encoded in
    ISO-8859-1.

    :param fPath: The fPath to the input text file.
    :return: A list containing all the lines of the file read correctly.
    """
    with open(fPath, "r", encoding="ISO-8859-1") as inF:

        # Replacing non-breaking space in Latin1 with a UTF-8 space
        ls = inF.readlines()
        ls = [l.replace("\xa0", " ") for l in ls]
        return ls


def parse(data):
    """
    Parses the input of the Santander text file.

    The format of the bank statement is as follows:

       "From: <date> to <date>"

       "Account: <number>"

       "Date: <date>"
       "Description: <description>"
       "Amount: <amount>"
       "Balance: <amount>"

        <second_transaction_entry>

        <nth_transaction_entry>

    :param data: A list containing each line of the bank statement.
    :return: A pandas DataFrame.
    """
    dates = []
    descs = []
    amounts = []
    balances = []

    # Skip unnecessary headers
    data = data[4:]

    # Remove empty lines
    data = [d.strip() for d in data]
    data = list(filter(None, data))

    # Creates sublist for each transaction
    data = [data[d:d+4] for d in range(0, len(data), 4)]

    # Parsing data into a 2D list
    for entry in data:
        # Removing field descriptors
        for e in entry:

            if e.startswith("Date"):
                dates.append(e.replace("Date: ", "").strip())

            if e.startswith("Description"):
                descs.append(e.replace("Description: ", "").strip())

            if e.startswith("Amount"):
                amounts.append(e.replace("Amount: ", "")
                                .replace(" GBP", "").strip())

            if e.startswith("Balance"):
                balances.append(e.replace("Balance: ", "")
                                 .replace(" GBP", "").strip())

    # Stores data in a Pandas data container
    parsed = pd.DataFrame({"DATES": dates,
                           "DESCRIPTION": descs,
                           "AMOUNT": amounts,
                           "BALANCE": balances})
    return parsed


def swapColumns(entries):
    """
    Changes the order of the columns that are stored in the given panadas
    object (usually to increase human readability of output).

    :param entries: A pandas DataFrame.
    :return: A dictionary mapping line numbers to transaction entries.
    """
    cols = entries.columns.tolist()
    swapped = [cols[0], cols[3], cols[2], cols[1]]
    entries = entries[swapped]
    return entries
