import os
import pandas as pd
import unittest
import monies.monies.santander as san


def disabled(f):
    def _decorator():
        print(f.__name__ + ' has been disabled')
    return _decorator


class TestUnit(unittest.TestCase):

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

        header = ["DATE", "DESCRIPTION", "AMOUNT", "BALANCE"]
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

        self.dfParsed = pd.DataFrame(parsedBody, columns=header)
        self.dfSwapped = pd.DataFrame(swappedBody, columns=header)

    def testParse(self):
        if not self.dfParsed.equals(san.parse(self.rawData)):
            self.fail("The DataFrames are not equal!")

    def testSwapColumns(self):
       if not self.dfSwapped.equals(san.swapColumns(self.dfParsed)):
           self.fail("The DataFrames are not equal!")



class TestIntegration(unittest.TestCase):

    def testParseSantanderFile(self):
        iPath = os.path.join("..", "res", "san_input.txt")

        data = san.readFile(iPath)
        data = san.parse(data)
        data = san.swapColumns(data)

        expected = \
        {
            0: ["DATE", "BALANCE", "AMOUNT", "DESCRIPTION"],
            1: ["29/12/2012",
                "3472.63",
                "-10.45",
                "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
                "RATE 1.00/GBP ON 26-12-2012"],
            2: ["29/12/2012",
                "3472.63",
                "-10.45",
                "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
                "RATE 1.00/GBP ON 26-12-2012"],
        }

        self.assertDictEqual(data, expected)


