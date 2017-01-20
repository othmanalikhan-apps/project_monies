import os
import pandas as pd
import unittest
import monies.monies.santander as san


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(THIS_DIR, "res")


class SantanderInt(unittest.TestCase):

    def testParseSantanderFile(self):
        header = ["DATE", "BALANCE", "AMOUNT", "DESCRIPTION"]
        body = \
        [
            ["29/12/2012",
             "3472.63",
             "-10.45",
             "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
             "RATE 1.00/GBP ON 26-12-2012"],
            ["29/12/2012",
             "3472.63",
             "-10.45",
             "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
             "RATE 1.00/GBP ON 26-12-2012"],
        ]
        inp = pd.DataFrame(body, columns=header)

        iPath = os.path.join(DATA_PATH, "san_input.txt")
        out = san.readFile(iPath)
        out = san.parse(out)
        out = san.swapColumns(out)

        if not out.equals(inp):
            self.fail("The DataFrames are not equal!\n"
                      "Expected Header: {}\n"
                      "Actual Header: {}\n".format(inp.columns, out.columns))
