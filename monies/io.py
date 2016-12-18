"""
A script responsible for IO handling of Santander text files of bank
statements.
"""


def parse(data):
    """
    Parses the input of the Santander .txt file into CSV format.

    The format of the bank statement is as follows:

       "From: <date> to <date>"

       "Account: <number>"

       "Date: <date>"
       "Description: <description>"
       "Amount: <amount>"
       "Balance: <amount>"

        <second_transaction_entry>

    :param data: A string of the text file data.
    :return: A parsed string in CSV format.
    """
    sep = 5 * " "
    csv = ""

    data = list(filter(None, data))         # Removes empty lines
    data = data[2:]                         # Skip headers

    # Removing field descriptions
    for i, d in enumerate(data):
        if d.startswith("Date"):
            data[i] = d.replace("Date: ", "").strip()

        if d.startswith("Description"):
            data[i] = d.replace("Description: ", "").strip()

        if d.startswith("Amount"):
            data[i] = d.replace("Amount: ", "").replace(" GBP", "").strip()

        if d.startswith("Balance"):
            data[i] = d.replace("Balance: ", "").replace(" GBP", "").strip()

    # Builds CSV string
    for i, d in enumerate(data, start=1):
        if i % 4 == 0:
            csv = csv + d + "\n"
        else:
            csv = csv + d + sep

    return csv


