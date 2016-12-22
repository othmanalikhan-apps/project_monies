"""
Unit and integration tests for the monies module.
"""
import os
import filecmp
import unittest
import monies.monies.monies as m


def disabled(f):
    def _decorator():
        print(f.__name__ + ' has been disabled')
    return _decorator


class TestUnit(unittest.TestCase):

    def testParse(self):

        input = \
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
        self.assertEquals(m.parse(input), out)


class TestIntegration(unittest.TestCase):

    @disabled
    def testParseFile(self):
        iPath = os.path.join("..", "res", "san_input.txt")
        oPath = os.path.join("..", "res", "san_output.txt")
        ePath = os.path.join("..", "res", "san_expected.txt")

        m.parseFile(iPath, oPath)

        if not filecmp.cmp(ePath, oPath, shallow=False):
            self.fail("Files are not equal")
