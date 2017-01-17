"""
A script responsible for visualising money expenditure from bank statements.
"""
import math

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mdates


def query(entries, keyWord):
    """
    Filters out entries that match the given substring in the DESCRIPTION
    column.

    :param entries: A pandas Dataframe containing transaction entries.
    :param keyWord: The substring that is searched in the description column.
    :return: A pandas Dataframe containing matched transaction entries only.
    """
    return entries[entries["DESCRIPTION"].str.contains(keyWord, na=False)]

def categorise(entries, categories):
    """
    For the given categories, searches the entries and categorises the
    results.

    :param entries: A pandas Dataframe containing transaction entries.
    :param categories: A list with entries as (Title, searchWord),
    indicating categories to be searched.
    :return: A list containing DataFrame objects for each searched category.
    """
    found = [(title, query(entries, keyWord)) for title, keyWord in categories]
    return found

# TODO: Fix broken function
def plotTimeGraph(entries):
    """
    For each entry, plots a time against money expenditure graph.

    For instance, this method can plot time vs money graph for 'Food')

    :param data: A list with entries as (title, dates, amounts) for each
    category.
    """
    fig = plt.figure(figsize=(10, 10))
    fig.canvas.set_window_title("Expense Visualiser")

    # Formats both axis to be easier to read
    def formatAxis(ax):
        myFmt = mdates.DateFormatter('%b %d')
        ax.xaxis.set_major_formatter(myFmt)

        yLabels = ["£{:,.0f}".format(l) for l in ax.get_yticks()]
        ax.set_yticklabels(yLabels)

    # Settings subplots to be in a 2 x N grid
    rows = 2
    cols = math.ceil(len(data) / rows)

    # Finding global max and min for x-axis
    dss = [dates for _, dates, _ in data]
    xMax = max([max(ds) for ds in dss])
    xMin = min([min(ds) for ds in dss])

    # Adds a plot per category
    for i, (title, dates, amounts) in enumerate(data, start=1):
        ax = fig.add_subplot(cols, rows, i)
        ax.set_title(title)
        plt.xticks(rotation=45)

        ax.plot(dates, amounts, linewidth=2, c="red")
        ax.set_xlim(xMin, xMax)
        formatAxis(ax)

    fig.tight_layout()
    plt.show()


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


def main():
    """
    Runs the script
    """
    import os
    import monies.monies.santander as san

    iPath = os.path.join("..", "res", "ledgers", "2015.txt")
    #iPath = os.path.join("..", "res", "ledgers", "test.txt")

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

    categorise(entries, categories)
    #plotTimeGraph(categories(categories, entries))


if __name__ == "__main__":
    main()
