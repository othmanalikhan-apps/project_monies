"""
A script responsible for visualising money expenditure from bank statements.
"""
import math
import datetime

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates as mdates


def query(entries, keyWord):
    """
    Filters out entries that match the given 'contains' substring in the
    DESCRIPTION column.

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


def extractPlotData(entries):
    """
    Converts the given entries into a suitable form so that it can be plotted
    directly using matplotlib functions.

    :param entries: A dictionary mapping line numbers to transaction entries.
    :return: A tuple containing DATE and AMOUNT entries as tuples.
    """
    data = []
    entries.pop(0)      # Removes header

    for line, entry in entries.items():
        d, _, a, _ = entry

        point = (datetime.datetime.strptime(d, "%d/%m/%Y"), float(a))
        data.append(point)

    data = sorted(data, key=lambda x: x[0])     # Sorts based on dates
    dates, amounts = zip(*data)
    return dates, amounts


def search(categories, entries):
    """
    Searches the entries for the given categories.

    :param categories: A list of the form (Title, searchWord)
    :param entries: A dictionary mapping line numbers to transaction entries.
    :return: A list with entries as (title, dates, amounts) for each category.
    """
    found = []

    for title, keyWord in categories:
        dates, amounts = extractPlotData(query(entries, keyWord))
        f = (title, dates, amounts)
        found.append(f)

    return found


def write(entries, fPath):
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


def plot(data):
    """
    Plots multiple subplots where each subplot corresponds to a expenditure
    category (e.g. 'Food').

    :param data: A list with entries as (title, dates, amounts) for each
    category.
    """
    fig = plt.figure(figsize=(10, 10))
    fig.canvas.set_window_title("Expense Visualiser")

    rows = 2
    cols = math.ceil(len(data) / rows)

    # Formats both axis to be easier to read
    def formatAxis(ax):
        myFmt = mdates.DateFormatter('%b %d')
        ax.xaxis.set_major_formatter(myFmt)

        yLabels = ["£{:,.0f}".format(l) for l in ax.get_yticks()]
        ax.set_yticklabels(yLabels)

    for i, (title, dates, amounts) in enumerate(data, start=1):
        ax = fig.add_subplot(cols, rows, i)
        ax.set_title(title)
        plt.xticks(rotation=45)

        ax.plot(dates, amounts)
        formatAxis(ax)

    fig.tight_layout()
    plt.show()


def main():
    """
    Runs the script
    """
    import os
    import monies.monies.santander as san

    iPath = os.path.join("..", "res", "ledgers", "2015.txt")

    categories = \
    [
        #(Title, KeyWord)
        ("Food", "JUST EAT"),
        ("Aramco", "ARAMCO"),
        ("Paypal", "PAYPAL"),
        ("Tesco", "TESCO"),
        ("Misc", ""),
    ]

    entries = san.readFile(iPath)
    entries = san.parse(entries)
    entries = san.swapColumns(entries)
    plot(search(categories, entries))


if __name__ == "__main__":
    main()
