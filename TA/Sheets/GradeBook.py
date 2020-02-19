from TA.Login.Login import Login , Browser
from TA.Sheets.utils import CanvasURLS
from TA.Conf import Config
from TA.Login.BrowserInteractions import BrowserInteractionsSingleton


import os
from pathlib import Path
import argparse
import pandas as pd

class GradeBook:

    def DownloadGradeBook(self,courseId , downloadFolder):
        url = CanvasURLS.GetCourseGradeBookURL(courseId)
        actionCssSelector = "span[data-component='ActionMenu']"
        exportCssSelector= "span[data-menu-id='export']"

        Browser(True,{"downloadFolder" : downloadFolder})

        browser = Login.GetBrowser(url , actionCssSelector)

        BrowserInteractionsSingleton().Click(browser,actionCssSelector)
        BrowserInteractionsSingleton().Click(browser,exportCssSelector)

    def _findFile(self,path):
        if os.path.exists(path):
            return path

        for file in os.listdir(Config.DATA_DUMP_FOLDER):
            if file.find(path) > -1:
                return os.path.abspath(os.path.join(Config.DATA_DUMP_FOLDER , file))

    def Analysis(self,pathToCSV):
        path = self._findFile(pathToCSV)
        df = pd.read_csv(path)
        df = df.loc[1:,]
        print(f"Total Students {df.shape[0]}")
        print(df["Unposted Current Grade"].value_counts())

        print(df.apply(lambda x : len(x[x == 0])))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--courseId" ,type=int, help="Copy courseid from the Course URL in canvas")
    parser.add_argument("--downloadFolder" ,type=str, default=Config.DATA_DUMP_FOLDER, help="Path to download location")
    parser.add_argument("--analysis" ,type=str, default="", help="Path to the grade book. Or a file name in the Data dump folder")

    args = parser.parse_args()
    if args.courseId:
        GradeBook().DownloadGradeBook(args.courseId , args.downloadFolder)
    if args.analysis:
        GradeBook().Analysis(args.analysis)
    #Python Online course 87897
    #Internship 118638
