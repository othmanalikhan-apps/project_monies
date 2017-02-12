"""
A script responsible for visualising money expenditure from bank statements.
"""
import os
import datetime
import numpy as np
import pygal

from pygal import style


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


def sliceMonthly(df):
    """
    Slices the given DataFrame whose index contains dates into monthly chunks.

    :param df: A pandas DataFrame object that contains transaction information.
    :return: A list of DataFrame objects that contain monthly transactions.
    """
    return [df.loc[df.index.month == m] for m in range(1, 13)]


def plotMonthlyBarChart(data, outDir):
    """
    For each entry, plots a time against money expenditure graph.

    For instance, this method can plot time vs money graph for 'Food')

    :param data: A list containing the title and DataFrame object for each
    searched category.
    :param outDir: The output directory to store the generated plot file.
    """
    # Initialising beautiful plot format
    config = pygal.Config()
    config.style = pygal.style.BlueStyle
    config.human_readable = True
    config.legend_at_bottom = True
    config.value_formatter = lambda y: "{:.0f} GBP".format(y)
    config.x_labels = ["Jan", "Feb", "Mar", "Apr", "May", "June",
                       "July", "Aug", "Sep", "Oct", "Nov", "Dec"]
    config.title = "Monthly Expense Breakdown"

    plot = pygal.Bar(config)

    # Preparing all data frames for plotting
    for title, df in data:
        dfs = sliceMonthly(df)
        balances = [sum(df["AMOUNT"]) for df in dfs]
        plot.add(title, balances)

    # Adds spacing between bars (hacky solution as no alternatives found)
    plot.add("Space", len(config.x_labels)*[])

    # Save the plot to a file
    plot.render_to_file(os.path.join(outDir, 'monthly_bar_chart.svg'))


def plotBalanceVsTime(data):
    """
    Plots the total balance against time for multiple lines where each line
    represents a category within the data.

    :param data: A list containing a title and a DataFrame object for each
    category.
    """
    # Initialising beautiful plot format
    config = pygal.Config()
    config.human_readable = True
    config.x_label_rotation = 35
    config.x_value_formatter = lambda dt: dt.strftime('%Y-%m-%d')
    config.value_formatter = lambda y: "{:.0f} GBP".format(y)

    plot = pygal.DateTimeLine(config)

    def prepareDFPlot(df):
        plotData = []
        for i, row in df.iterrows():
            d = datetime.datetime.strptime(row["DATE"], "%d/%m/%Y")
            b = float(row["AMOUNT"])
            plotData.append((d, b))
        return plotData

    # Preparing all data frames for plotting
    for title, df in data:
        plot.add(title, sorted(prepareDFPlot(df)))

    # Save the plot to a file
    plot.render_to_file('balance_vs_time.svg')


#TODO: Change so that it writes categories (i.e. filename = category + date)
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
        np.savetxt(outF, np.array(entries), delimiter=dFormat)



def main():
    """
    Runs the script
    """
    import os
    import monies.monies.santander as san

    iPath = os.path.join("..", "res", "ledgers", "2015.txt")
    oPath = os.path.join("..", "res", "ledgers", "2015_output.txt")
    #iPath = os.path.join("..", "res", "ledgers", "test.txt")
    oDir = os.path.join("..", "res", "output")

    categories = \
    [
        # (Title, KeyWord)
        ("Food", "JUST EAT"),
        # ("Aramco", "ARAMCO"),
        # ("Paypal", "PAYPAL"),
        ("Tesco", "TESCO"),
        # ("Misc", ""),
    ]

    entries = san.readFile(iPath)
    entries = san.parse(entries)
    entries.to_csv()

    plotData = categorise(entries, categories)
    plotMonthlyBarChart(plotData, oDir)
    # plotBalanceVsTime(plotData)


if __name__ == "__main__":
    main()


# BLUEPRINT
# =========
#
# What: Monthly bar plot
# Details: For every month, all categories vs total expense
# Why: Find cheapest food ordering scheme
#
# What: Yearly line plot
# Details: Total expense vs time for all categories
# Why: Predict in how many years I can buy item X
# Why: Highlight category with highest expense so that I can cut it.
#
# What: Yearly line plot
# Details: Total expense vs time for all categories
# Why: Estimate total cash in bank after X years
