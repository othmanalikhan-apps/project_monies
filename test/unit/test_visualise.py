import os
import filecmp
import unittest
import datetime
import pandas as pd

import monies.monies.visualise as vis


def disabled(f):
    def _decorator():
        print(f.__name__ + ' has been disabled')
    return _decorator


class TestUnit(unittest.TestCase):

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

    def _assertDataFrames(self, exp, out):
        if not out.equals(exp):
            self.fail("EXPECTED:\n{}\n\n\n"
                      "ACTUAL:\n{}\n\n\n".format(exp, out))



class TestIntegration(unittest.TestCase):

    def testWriteData(self):
        data = \
        {
            0: ["DATE", "BALANCE", "AMOUNT", "DESCRIPTION"],
            1: ["29/12/2012",
                "3472.63",
                "-10.45",
                "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
                "RATE 1.00/GBP ON 26-12-2012"],
            2: ["28/12/2012",
                "3483.08",
                "-10.00",
                "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
                "RATE 1.00/GBP ON 26-12-2012"]
        }

        oPath = os.path.join("..", "res", "san_output.txt")
        ePath = os.path.join("..", "res", "san_expected.txt")

        vis.write(data, oPath)
        self.assertTrue(filecmp.cmp(oPath, ePath))
