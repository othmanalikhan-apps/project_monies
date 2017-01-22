"""
A script responsible for visualising money expenditure from bank statements.
"""
import datetime
import pygal
import numpy as np


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
    For each category, queries the entries and then stores the preferred
    title of the query and its data.

    :param entries: A pandas Dataframe containing transaction entries.
    :param categories: A list with entries as (Title, searchWord),
    indicating categories to be searched.
    :return: A list containing the preferred title and DataFrame object for
    each searched category.
    """
    found = [(title, query(entries, keyWord)) for title, keyWord in categories]
    return found


def sliceMonthly():
    pass


# TODO: WORKING ! ! !
# Time (over several months) vs instantaneous expenditure
# Time (over several months) vs cumulative expenditure

# Time (month) vs instantaneous expenditure
# Time (month) vs cumulative expenditure

# Bar chart of cumulative expenditure (every month) of a certain category

# Compare monthly data for specific categories (e.g. Just Eat in Month 1 vs
# Just Eat in Month 2) and find month with the least spent amount
def plotTimeGraph(data):
    """
    For each entry, plots a time against money expenditure graph.

    For instance, this method can plot time vs money graph for 'Food')

    :param data: A list containing the title and DataFrame object for each
    searched category.
    """

    config = pygal.Config()
    config.human_readable = True

    plot = pygal.DateTimeLine(config)

    for title, df in data:
        plotData = []

        for i, row in df.iterrows():
            d = datetime.datetime.strptime(row["DATE"], "%d/%m/%Y")
            b = float(row["AMOUNT"])
            plotData.append((d, b))

        plotData = sorted(plotData)
        plot.add(title, plotData)

    plot.render_to_file('bar_chart.svg')  # Save the svg to a file


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

    plotData = categorise(entries, categories)
    plotTimeGraph(plotData)


if __name__ == "__main__":
    main()
