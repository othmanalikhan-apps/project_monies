import unittest
import datetime

import pandas as pd
from pandas.util.testing import assert_frame_equal

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

        pHeader = ["DATES", "BALANCE", "AMOUNT", "DESCRIPTION"]
        parsedBody = \
        [
            [datetime.datetime(2012, 12, 29),
             3472.63,
             -10.45,
             "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
             "RATE 1.00/GBP ON 26-12-2012"],
            [datetime.datetime(2012, 12, 28),
             3483.08,
             -10.00,
             "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
             "RATE 1.00/GBP ON 26-12-2012"]
        ]

        self.dfParsed = pd.DataFrame(parsedBody, columns=pHeader)

    def testParse(self):
        inp = san.parse(self.rawData)
        out = self.dfParsed
        assert_frame_equal(inp, out)
