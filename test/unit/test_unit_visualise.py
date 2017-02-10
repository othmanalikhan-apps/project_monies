import unittest
import datetime as dt

import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal

import monies.monies.visualise as vis


def disabled(func):
    def _wrapper(f):
        print(str(f) + " test is disabled!")
    return _wrapper(func)


class VisualiseUnit(unittest.TestCase):

    def setUp(self):
        header = ["DATE", "BALANCE", "AMOUNT", "DESCRIPTION"]
        self.dfInp = self.setupDefault(header)
        self.dfQuery = self.setupQuery(header)
        self.dfPlot = self.setupPlot(header)
        self.dfCategories = self.setupCategorise(header)

    def setupDefault(self, header):
        body = \
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
             "RATE 1.00/GBP ON 26-12-2012"],
            ["28/12/2011",
             "1344.08",
             "23.00",
             "CARD PAYMENT TO WWW.UCAS.COM,23.00 GBP, RATE 1.00/GBP ON "]
        ]
        return pd.DataFrame(body, columns=header)

    def setupQuery(self, header):
        body = \
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
             "RATE 1.00/GBP ON 26-12-2012"],
        ]
        return pd.DataFrame(body, columns=header)

    def setupPlot(self, header):
        body = \
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
             "RATE 1.00/GBP ON 26-12-2012"],
            ["27/12/2012",
             "3483.08",
             "-14.00",
             "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
             "RATE 1.00/GBP ON 26-12-2012"],
        ]
        return pd.DataFrame(body, columns=header)

    def setupCategorise(self, header):
        body = \
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
             "RATE 1.00/GBP ON 26-12-2012"],
        ]
        return [("Food", pd.DataFrame(body, columns=header))]

    def testQuery(self):
        exp = self.dfQuery
        out = vis.query(self.dfInp, "JUST EAT")

        self._assertDataFrames(exp, out)

    def testCategorise(self):
        exp = self.dfCategories
        out = vis.categorise(self.dfInp, [("Food", "JUST EAT")])

        for i in range(max(len(out), len(exp))):
            _, dfOut = out[i]
            _, dfExp = exp[i]
            self._assertDataFrames(dfExp, dfOut)

    def testSliceMonthly(self):

        def _generateMonthData(month):
            days = pd.date_range(dt.datetime(2015, month+1, 1),
                                 dt.datetime(2015, month, 1))
            data = np.random.rand(len(days))
            month = pd.DataFrame({"BALANCE": data,
                                  "AMOUNT": data,
                                  "DESCRIPTION": data},
                                 index=days)
            return month

        jan = _generateMonthData(1)
        feb = _generateMonthData(2)
        mar = _generateMonthData(3)
        allMonths = jan + feb + mar

        months = vis.sliceMonthly(allMonths)

        assert_frame_equal(months[0], jan)
        assert_frame_equal(months[1], feb)
        assert_frame_equal(months[2], mar)

    def _assertDataFrames(self, exp, out):
        if not out.equals(exp):
            self.fail("EXPECTED:\n{}\n\n\n"
                      "ACTUAL:\n{}\n\n\n".format(exp, out))

