import filecmp
import os
import unittest
import monies.monies.visualise as vis


def disabled(f):
    def _decorator():
        print(f.__name__ + ' has been disabled')
    return _decorator


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

        vis.writeData(data, oPath)
        self.assertTrue(filecmp.cmp(oPath, ePath))


