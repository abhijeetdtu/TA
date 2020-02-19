from TA.Sheets.utils import CanvasURLS
from TA.Login.Login import Login

import pandas as pd
import argparse
from bs4 import BeautifulSoup
import json
import seaborn as sns
import matplotlib.pyplot as plt

class CourseAnalytics:

    def _stripStr(self,jsStr):
        return jsStr.text.replace("while(1);" , "")

    def StudentAnalytics(self , courseId):
        url = CanvasURLS.GetCourseAnalyticsStudentURL(courseId)
        jsStr = Login.StaticAuthGet(url)
        jsStr = self._stripStr(jsStr)
        df = pd.read_json(jsStr)
        df[["page_views" , "participations"]].describe().to_csv(f"./tmp_student_{courseId}.csv")

    def _flattenTardiness(self , js):
        TARDY = 'tardiness_breakdown'
        TOTAL = "total"
        all = []
        for t in js:
            obj = {}
            obj["title"] = t["title"]
            for k in t[TARDY].keys():
                if k != TOTAL:
                    obj[f"submission_{k}"] = int(t[TARDY][TOTAL]) * float(t[TARDY][k])
                else:
                    obj[f"total_students"] = t[TARDY][TOTAL]

            all.append(obj)
        return all

    def AssignmentAnalytics(self,courseId):
        ONTIME = "submission_on_time"
        TITLE = "title"
        SUBMI = "Submissions"

        url = CanvasURLS.GetCourseAnalyticsAssignmentURL(courseId)
        jsStr = Login.StaticAuthGet(url)
        jsStr = self._stripStr(jsStr)
        js = json.loads(jsStr)
        njs = self._flattenTardiness(js)
        df = pd.read_json(json.dumps(njs) , orient= "records")
        df = df.sort_values(ONTIME , ascending=False)
        df = df.rename({ONTIME:SUBMI} , axis=1)

        #plt.tight_layout()
        plt.subplots_adjust(left=0.6)
        plt.title("Submissions Per Assignment")

        sns.barplot(x=SUBMI , y = TITLE , data=df[[TITLE,SUBMI]])

        plt.show()

    def Run(self , courseId):
        self.StudentAnalytics(courseId)
        self.AssignmentAnalytics(courseId)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--courseId" ,type=int, help="Copy courseid from the Course URL in canvas")

    args = parser.parse_args()
    CourseAnalytics().Run(args.courseId)
