import os
import unittest
import monies.monies.santander as san


def disabled(f):
    def _decorator():
        print(f.__name__ + ' has been disabled')
    return _decorator


class TestUnit(unittest.TestCase):

    def testParse(self):

        inp = \
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

        out = \
        {
            0: ["DATE", "DESCRIPTION", "AMOUNT", "BALANCE"],
            1: ["29/12/2012",
                "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
                "RATE 1.00/GBP ON 26-12-2012",
                "-10.45",
                "3472.63"],
            2: ["28/12/2012",
                "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
                "RATE 1.00/GBP ON 26-12-2012",
                "-10.00",
                "3483.08"]
        }
        self.assertDictEqual(san.parse(inp), out)

    def testSwapColumns(self):

        inp = \
        {
            0: ["DATE", "DESCRIPTION", "AMOUNT", "BALANCE"],
            1: ["29/12/2012",
                "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
                "RATE 1.00/GBP ON 26-12-2012",
                "-10.45",
                "3472.63"],
            2: ["28/12/2012",
                "CARD PAYMENT TO WWW.JUST EAT.CO.UK,10.45 GBP, "
                "RATE 1.00/GBP ON 26-12-2012",
                "-10.00",
                "3483.08"]
        }

        out = \
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

        self.assertDictEqual(san.swapColumns(inp), out)


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


