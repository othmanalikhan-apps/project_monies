"""
A script responsible for parsing bank statement files from Santander.

The files are text files with ISO-8859-1 encoding written in a specific format.
"""


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
    :return: A dictionary mapping line numbers to data entries.
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


def swapColumns(entries):
    """
    Changes the order of the columns that are stored in the dictionary (i.e.
    changes the order of the elements of the dictionary values which are lists).

    :param entries: A dictionary mapping line numbers to data entries.
    :return: A dictionary mapping line numbers to data entries.
    """
    for num, entry in entries.items():
        date, desc, amount, balance = entry
        entries[num] = [date, balance, amount, desc]

    return entries
