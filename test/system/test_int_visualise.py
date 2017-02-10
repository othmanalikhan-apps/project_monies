import os
import filecmp
import unittest
import monies.monies.visualise as vis


# Declaring paths
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(THIS_DIR, "res")


class VisualiseInt(unittest.TestCase):

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

        oPath = os.path.join(DATA_PATH, "san_output.txt")
        ePath = os.path.join(DATA_PATH, "san_expected.txt")

        vis.write(data, oPath)
        self.assertTrue(filecmp.cmp(oPath, ePath))
