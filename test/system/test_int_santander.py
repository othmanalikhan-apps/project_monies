import os
import unittest
import datetime
import pandas as pd
from pandas.util.testing import assert_frame_equal
import monies.monies.santander as san


# Declaring test resource path
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(THIS_DIR, "res")


class SantanderInt(unittest.TestCase):

    def testParseSantanderFile(self):
        header = ["DATES", "BALANCE", "AMOUNT", "DESCRIPTION"]
        body = \
        [
            [datetime.datetime(2012, 12, 29),
             3472.63,
             -10.45,
             "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
             "RATE 1.00/GBP ON 26-12-2012"],
            [datetime.datetime(2012, 12, 29),
             3472.63,
             -10.45,
             "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
             "RATE 1.00/GBP ON 26-12-2012"],
        ]
        inp = pd.DataFrame(body, columns=header)

        iPath = os.path.join(DATA_PATH, "san_input.txt")
        out = san.readFile(iPath)
        out = san.parse(out)

        assert_frame_equal(inp, out)
