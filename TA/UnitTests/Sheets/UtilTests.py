import unittest

from TA.Sheets.utils import *


class UtilsTests(unittest.TestCase):

    def test_ExcelDiff(self):
        ExcelDiff("./TA/DataDump/Tracker_2020_01_28_19_45_33.xlsx" ,"./TA/DataDump/Tracker.xlsx" , "CanvasId"  )


if __name__ == "__main__":
    unittest.main()
