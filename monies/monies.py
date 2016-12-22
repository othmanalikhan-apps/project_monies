"""
A script responsible for parsing bank statement files, specifically for
Santander text files, and visualising where the money is being used to
better understand where it can be saved.
"""


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


def parseFile(iPath, oPath):
    """
    Parses the file for the given path into CSV format (it is assumed the
    file is a Santander .txt file with ISO-8859-1 encoding).

    :param iPath: The path to the input text file.
    :param oPath: The path to the output csv file.
    """
    with open(iPath, "r", encoding="ISO-8859-1") as i, \
         open(oPath, "w", encoding="UTF-8") as o:

        # Replacing non-breaking space in Latin1 with a UTF-8 space
        ls = i.readlines()
        ls = [l.replace("\xa0", " ") for l in ls]

        o.write(parse(ls))




# iPath = os.path.join("..", "res", "ledgers", "2012.txt")
# oPath = os.path.join("..", "res", "ledgers", "2012.csv")
# parseFile(iPath, oPath)
