import pandas as pd
import unittest
import monies.monies.santander as san


class SantanderUnit(unittest.TestCase):

    def setUp(self):
        self.rawData = \
        [
            "From: 31/12/2011 to 31/12/2012\n",
            "\n",
            "Account: XXXX XXXX XXXX XXXX\n",
            "\n",
            "Date: 29/12/2012\n",
            "Description: CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, RATE 1.00/GBP ON 26-12-2012\n",
            "Amount: -10.45 GBP\n",
            "Balance: 3472.63 GBP\n",
            "\n",
            "Date: 28/12/2012\n",
            "Description: CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, RATE 1.00/GBP ON 26-12-2012\n",
            "Amount: -10.00\n",
            "Balance: 3483.08 GBP"
        ]

        pHeader = ["DATE", "DESCRIPTION", "AMOUNT", "BALANCE"]
        parsedBody = \
        [
            ["29/12/2012",
             "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
             "RATE 1.00/GBP ON 26-12-2012",
             "-10.45",
             "3472.63"],
            ["28/12/2012",
             "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
             "RATE 1.00/GBP ON 26-12-2012",
             "-10.00",
             "3483.08"]
        ]

        sHeader = ["DATE", "BALANCE", "AMOUNT", "DESCRIPTION"]
        swappedBody = \
        [
            ["29/12/2012",
             "3472.63",
             "-10.45",
             "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
             "RATE 1.00/GBP ON 26-12-2012"],
            ["28/12/2012",
             "3483.08",
             "-10.00",
             "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
             "RATE 1.00/GBP ON 26-12-2012"]
        ]

        self.dfParsed = pd.DataFrame(parsedBody, columns=pHeader)
        self.dfSwapped = pd.DataFrame(swappedBody, columns=sHeader)

    def testParse(self):
        inp = san.parse(self.rawData)
        out = self.dfParsed

        if not out.equals(inp):
            self.fail("The DataFrames are not equal!")

    def testSwapColumns(self):
        inp = san.swapColumns(self.dfParsed)
        out = self.dfSwapped

        if not out.equals(inp):
            self.fail("The DataFrames are not equal!\n"
                      "Expected Header: {}\n"
                      "Actual Header: {}\n".format(inp.columns, out.columns))
