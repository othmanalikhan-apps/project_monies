"""
A script responsible for parsing bank statement files from Santander. The
files are text files with ISO-8859-1 encoding, written in a specific format.
"""
import numpy as np


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
    :return: A dictionary containing the parsed entries.
    """
    HEADER = ["DATE", "DESCRIPTION", "AMOUNT", "BALANCE"]
    parsed = {0: HEADER}

    # Skip unnecessary headers
    data = data[4:]

    # Remove empty lines
    data = [d.strip() for d in data]
    data = list(filter(None, data))

    # Creates sublist for each transaction
    data = [data[d:d+4] for d in range(0, len(data), 4)]

    # Parsing into dictionary
    for i, entry in enumerate(data, start=1):
        parsed[i] = []

        # Removing field descriptors
        for e in entry:

            if e.startswith("Date"):
                e = e.replace("Date: ", "").strip()

            if e.startswith("Description"):
                e = e.replace("Description: ", "").strip()

            if e.startswith("Amount"):
                e = e.replace("Amount: ", "").replace(" GBP", "").strip()

            if e.startswith("Balance"):
                e = e.replace("Balance: ", "").replace(" GBP", "").strip()

            parsed[i].append(e)

    return parsed


def toCSV(iPath, oPath):
    """
    Parses a text file (A Santander bank statement file encoded in ISO-8859-1
    encoding) and converts it into an CSV file.

    :param iPath: The path to the input text file.
    :param oPath: The path to the output csv file.
    """
    with open(iPath, "r", encoding="ISO-8859-1") as inF, \
            open(oPath, "wb") as outF:

        # Replacing non-breaking space in Latin1 with a UTF-8 space
        ls = inF.readlines()
        ls = [l.replace("\xa0", " ") for l in ls]

        entries = [entry for i, entry in sorted(parse(ls).items())]

        # Re-ordering columns
        for i, entry in enumerate(entries):
            date, desc, amount, balance = entry
            entries[i] = [date, balance, amount, desc]

        # Writing data using numpy
        entries = np.array(entries)
        dFormat = "%10s {0} %9s {0} %8s {0} %s".format(3*" ")
        np.savetxt(outF, np.array(entries), fmt=dFormat)
