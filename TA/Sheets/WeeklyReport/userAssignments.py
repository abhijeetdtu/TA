# %load_ext autoreload
# %autoreload 2

from multiprocessing.dummy import Pool as ThreadPool
from TA.Login.Login import Login
from TA.Sheets.WeeklyReport.apiEndpoints import ENDPOINTS
from TA.Sheets.WeeklyReport.userList import CourseUsers
from TA.Sheets.WeeklyReport.assignments import CourseAssignments

import os
import json
import csv
import pickle
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
import logging
from datetime import date
from datetime import datetime as dtime
from plotnine import *
import re

logging.basicConfig(level=logging.INFO)

class CourseUserSubmissions:

    class AssignmentDetails:

        def __init__(self,name,due,status,score,points,details,submissionUrl):
            self.name = name
            self.due = due
            self.status = status
            self.score = score
            self.points = points
            self.details = details
            self.submissionUrl = submissionUrl

    class consts:
        SUBMISSION_TIME = ".submission-details-header__time"
        SUBMISSION_GRADE = ".grading_value.grading_box"

        # GRADES_TABLE = "#grades_summary"
        # TABLE_ROW = ".student_assignment"
        # FINAL_GRADE = "#submission_final-grade"
        # ASN_DUE = ".due"
        # ASN_STATUS = ".status"
        # ASN_SCORE = "div.score_holder span.grade"
        # ASN_PSBL_POINTS = ".points_possible"
        # ASN_DETAILS = ".details"
        #
        # ASN_ALL = [ASN_DUE,ASN_STATUS,ASN_SCORE,ASN_PSBL_POINTS,ASN_DETAILS]
        # ASN_ALL_TITLES = ["Assignment Due"
        #                 , "Assignment Status"
        #                 , "Assignment Score"
        #                 , "Assignment Possible Points"
        #                 , "Assignment Details"]

    def __init__(self,courseId , reportFolder):
        self.courseUsers = CourseUsers(courseId)
        self.courseId = courseId
        self.url = ENDPOINTS.USER_SUBMISSION

        self.reportFolder = reportFolder
        if not os.path.exists(reportFolder):
            os.mkdir(reportFolder)
        self.oFilePath = os.path.abspath(os.path.join(reportFolder, "grades.csv"))

        bgColorHex = "#25292f"
        mt = theme(panel_grid_major = element_blank()
                 , panel_grid_minor = element_blank()
                 ,panel_background = element_rect(fill = bgColorHex)
                 ,plot_background  = element_rect(fill =bgColorHex, colour = 'white')
                 ,axis_text = element_text( face = "bold", colour = "white",size = 8)
                 ,axis_title = element_text( face = "bold", colour = "white",size = 10)
                 ,legend_background = element_rect(fill =bgColorHex, colour = 'white'))

        self.plotTheme = mt

    def _pathInReportFolder(self,fname):
        return os.path.abspath(os.path.join(self.reportFolder, fname))

    def soupToAssignment(self ,name, text):
        try:
            soup = BeautifulSoup(text)
            date = soup.select_one(CourseUserSubmissions.consts.SUBMISSION_TIME).text
            grade = soup.select_one(CourseUserSubmissions.consts.SUBMISSION_GRADE).get("value")
        except:
            date = f"{name} submitted"
            grade = None

        date = date.replace(name, "").replace("submitted" , "").replace("\n" , "").strip(" ")

        return [date,grade]

    def soupToAssignments_(self , text):
        soup = BeautifulSoup(text)
        table = soup.select_one(consts.GRADES_TABLE)
        #table.select(consts.TABLE_ROW)

        assignments = []
        for tr in table.select(consts.TABLE_ROW) :
            if tr.select_one("th.title"):
                name = tr.find("a").text if tr.select_one("a") else  tr.select_one("th.title").text
                name = name.replace("\n" , "").strip(" ")
                details = [tr.select_one(selector).text.replace("\n" , "").strip(" ") for selector in consts.ASN_ALL]
                assignments.append(AssignmentDetails(name , *details))

        return assignments

    def assignmentToHeader(self,assignments):
        return [(a.name,a.score) for a in assignments]

    # def gradesToCSV(self, grades):
    #     grades = [assignments]
    #     header = self.assignmentToHeader(grades[0])
    #
    #     with open(self.oFilePath , "w") as f:
    #         writer = csv.writer(f)
    #         writer.writerow(header )
    #         writer.writerows(grades)

    def getAssignments(self,user,assignmentsList):
        grades = []
        userid = user["id"]
        name = user["name"]

        logging.info(f"{userid} - {name}")

        for assignment in assignmentsList:

            url = self.url.format(COURSE_ID=self.courseId , USER_ID = userid , ASSIGNMENT_ID=assignment[-1])
            resp = Login.StaticAuthGet(url)
            assignmentDetails = self.soupToAssignment(name,resp.text)
            print(assignmentDetails)

            #rows = [a.score for a in assignments]
            grades.append([name , assignment[2]]+ assignmentDetails)

        return grades

    def getList(self):
        # ca = CourseUsers(self.courseId)
        # an = ca.getList()
        # grades = []
        # assignmentsList = CourseAssignments(self.courseId).getAssignmentsList()
        #
        # pool = ThreadPool(5)
        # grades  = pool.map(lambda u : self.getAssignments(u,assignmentsList) , an)
        # #
        # pickle.dump(grades , open("grades_2.pkl" , "wb"))

        grades = pickle.load(open("grades_2.pkl" , "rb"))
        self.gradesToCSV(grades)

    def _filterDFOnDate(self,df):
        students = df.loc[np.where(df["col2"].apply(lambda x: x.find("05") > -1 ))]["col0"].unique()
        return df[df["col0"].isin(students)]

    def gradesToCSV(self,grades , filterDate = "04/20/2020"):

        gradesAll = [g for gi in grades for g in gi]

        df = pd.DataFrame(gradesAll , columns=[f"col{i}" for i in range(4)])

        def parseDate(date):
            try:
                dt= dtime.strptime(date , "%b %d at %I:%M%p %Y" )
            except:
                try:
                    dt= dtime.strptime(date , "%b %d at %I%p %Y")
                except:
                    dt= date(1992,1,1)
            return dt


        df["col2"] = df["col2"].str.replace("^\s*$" , "Jan 1 at 12:00pm" ,regex=True)
        df["col2"] = df["col2"] + " 2020"
        df["col2"] = df["col2"].apply(lambda x: parseDate(x))

        df["col3"] = df["col3"].fillna("0")
        df["col3"] = df["col3"].str.replace("^\s*$" , "0", regex=True)
        df["col3"] = df["col3"].astype("float")
        df["assignment_type"] = np.where(df["col1"].str.lower().str.find("knowledge check") > -1 , "kc" , "ex")

        #print(df.head())
        self._toDatePlot(df)
        #df["col3_temp"] = df["col3"]
        def aggStudent(df):
            total = df["col3"].astype("float").sum()
            num_completed = df[df["col3"] != 0].shape[0]
            df = df[df["col2"] == df["col2"].max()].head(1)

            df["total"] = total
            df["num_completed"] = num_completed
            return df


        df = df.groupby(["col0","assignment_type"]).apply(aggStudent)
            ##
        df = df[df["col2"] > dtime.strptime(filterDate , "%m/%d/%Y")]

        def pivotStudent(df):
            df = df.drop("assignment_type" , axis=1)
            if df.shape[0] == 1:
                filler = pd.Series(np.repeat("-" , df.shape[1]) , index=df.columns)
            else:
                filler = df.loc[1]
            df = pd.concat([df.iloc[0], filler])
            df = pd.DataFrame(df).transpose()
            return df

        s = df.reset_index(drop=True).groupby("col0").apply(pivotStudent)
        s.columns = [a + "_" + h for a in ["Latest Exercise" ,"Latest knowledge Check"] for h in ["Delete","Name" , "Submission Date" , "Score" ,"Total Score" , "Total Completed"] ]

        s = s.reset_index()
        s = s.rename(columns={ "col0" : "Student Name"
                    , "Latest Exercise_Total Score" : "All Exercises Total Score"
                    , "Latest Exercise_Total Completed" : "Total Exercises Completed"
                    , "Latest knowledge Check_Total Score" : "All Knowledge Checks Total Score"
                    , "Latest knowledge Check_Total Completed" : "Total Knowledges checks Completed" })

        s = s.drop([c for c in s.columns if c.find("Delete") > -1] + ["level_1"] , axis=1)

        s.to_csv(self.oFilePath ,index=False)
        #self.dfToPlot(dates,scores)


    def _toDatePlot(self,df):
        df = df.copy()
        df["date"] = df["col2"].dt.strftime("%m_%d_%y")
        df = df[df["date"] != "01_01_20"]
        d = df.groupby(["assignment_type","date"]).count().reset_index()
        print(d)
        p = ggplot(d , aes(x="date" , y="col0" , color="assignment_type",group="assignment_type"))\
         + geom_line()\
         + xlab("Date")\
         + ylab("Number of Submissions")\
         + self.plotTheme\
         + theme(axis_text_x=element_text(angle=-90) , legend_text=element_text(color="white"))
        p.save(self._pathInReportFolder("trend.png"))

    def _datePlot(self,dates):
        meltedDates = dates.melt()
        dateCounts = meltedDates.groupby("value").count().reset_index().sort_values("value")
        dateCounts = dateCounts[dateCounts["value"] != "-"]
        dateCounts["variable"] = dateCounts["variable"].astype("int")
        p = (ggplot(dateCounts , aes(x="value" , y="variable" , group=1)) +
        geom_line(color="white") +
        xlab("Date") +
        ylab("Number of Submissions") +
        self.plotTheme  +
        theme(axis_text_x=element_text(angle=-90)))

        p.save(self._pathInReportFolder("trend.png"))

    def _scorePlot(self,scores):
        scoresdf = scores.reset_index()
        scoresdf = scoresdf.drop(["num_completed"] , axis=1)
        scoresdf = scoresdf.melt(id_vars="col0").replace("-" , -1)
        scoresdf["value"] = scoresdf["value"].astype("float")

        scoresdf["value"].describe()
        p = (ggplot(scoresdf , aes(x="col1" , y="col0" , color="value")) +
        geom_point() +
        xlab("Assignment") +
        ylab("Student") +
        self.plotTheme +
        theme(figure_size=(10,20) , axis_text_x=element_text(angle=-90) , legend_text=element_text(color="white")))
        p.save(self._pathInReportFolder("grade_matrix.png"))

    def dfToPlot(self , dates,scores):
        self._datePlot(dates)
        self._scorePlot(scores)


if __name__ == "__main__":
    import argparse
    import pathlib
    import datetime

    """
    python -m TA.Sheets.WeeklyReport.userAssignments --course-id 87897
    """
    dpath = os.path.join(pathlib.Path(__file__).resolve().parent.absolute() , f"report_{datetime.date.today()}")
    parser = argparse.ArgumentParser()
    parser.add_argument("--course-id")
    parser.add_argument("--report-folder" , default=dpath)

    args = parser.parse_args()

    ca = CourseUserSubmissions(args.course_id , args.report_folder )
    an = ca.getList()
