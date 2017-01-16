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

        queryBody = \
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

        self.dfInp = pd.DataFrame(body, columns=header)
        self.dfQuery = pd.DataFrame(queryBody, columns=header)

    def testQuery(self):
        exp = self.dfQuery
        out = vis.query(self.dfInp, "JUST EAT")

        if not out.equals(exp):
            self.fail("EXPECTED:\n{}\n\n\n"
                      "ACTUAL:\n{}\n\n\n".format(exp, out))

    @disabled
    def testExtractPlotData(self):

        inp = \
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
                "RATE 1.00/GBP ON 26-12-2012"],
            3: ["27/12/2012",
                "3483.08",
                "-14.00",
                "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
                "RATE 1.00/GBP ON 26-12-2012"],
        }

        out = ((datetime.datetime(2012, 12, 27, 0, 0),
                datetime.datetime(2012, 12, 28, 0, 0),
                datetime.datetime(2012, 12, 29, 0, 0)),
               (-14.00,
                -10.00,
                -10.45))

        self.assertTupleEqual(vis.extractPlotData(inp), out)

    @disabled
    def testSearch(self):

        entries = \
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
                "RATE 1.00/GBP ON 26-12-2012"],
            3: ["28/12/2011",
                "1344.08",
                "23.00",
                "CARD PAYMENT TO WWW.UCAS.COM,23.00 GBP, RATE 1.00/GBP ON "]
        }

        categories = [("Food", "JUST EAT")]

        out = \
        [
            ("Food",
             (datetime.datetime(2012, 12, 28, 0, 0),
              datetime.datetime(2012, 12, 29, 0, 0)),
             (-10.00,
              -10.45))
        ]

        self.assertListEqual(vis.search(categories, entries), out)


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
