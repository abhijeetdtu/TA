from TA.Conf import Config

import os
import time

import pandas as pd

def PrintWithPad(val):
    print("\n\n---------------{}--------------\n\n".format(val))

class CanvasURLS:
    @staticmethod
    def GetCourseURL(courseId):
        return Config.baseCourseURL + f"/{courseId}"

    @staticmethod
    def GetCourseAssignmentURL(courseId):
        return Config.baseCourseURL + f"/{courseId}/assignments"

    @staticmethod
    def GetCourseGradeBookURL(courseId):
        return Config.baseCourseURL + f"/{courseId}/gradebook"

    @staticmethod
    def GetCourseAnalyticsStudentURL(courseId):
        #https://uncc.instructure.com/api/v1/courses/87897/analytics/student_summaries?page=1&per_page=1000
        return Config.studentSummaryAnalyticsURL.format(courseId)


    @staticmethod
    def GetCourseAnalyticsAssignmentURL(courseId):
        return Config.assignmentSummaryAnalyticsURL.format(courseId)

def DumpVersionedDF(filename , df,indexCol):
    folder = Config.DATA_DUMP_FOLDER
    name,extension = filename.split(".")
    filePath = os.path.abspath(os.path.join(folder ,filename))
    timestr = time.strftime("%Y_%m_%d_%H_%M_%S")
    newName = name + "_" + timestr + f".{extension}"
    diffName = name + "_" + timestr + f"_diff.{extension}"
    newPath = os.path.abspath(os.path.join(folder ,newName))
    diffPath =  os.path.abspath(os.path.join(folder ,diffName))

    if os.path.exists(filePath):
        os.rename(filePath , newPath)
    df.to_excel(filePath)
    diffDf = ExcelDiff(newPath , filePath , indexCol)
    if diffDf.shape[0] > 0:
        diffDf.to_excel(diffPath)

def ExcelDiff(f1 , f2 , indexCol):
    df1 = pd.read_excel(f1)
    df2 = pd.read_excel(f2)

    diffA = df1[df1 != df2]
    diffB = df2[df1 != df2]
    diffA = diffA.dropna(how="all")
    diffB = diffB.dropna(how="all")

    diff = diffA[~diffA.isna()] + " -> " + diffB[~diffA.isna()]
    diff = diff.join(df1 , lsuffix="_old" , rsuffix="_new")
    diff = diff.drop([c for c in diff.columns if c.find("_new") > -1 and c.find(indexCol) < 0] , axis=1)#pd.merge(diff, df1 , on="")
    print(f"Number of rows with changes {diff.shape[0]}")
    print(diff)
    return diff

class ColNames:
    MentorMailSentOn = "MentorMailSentOn"
    MentorLOAReceived = "MentorLOAReceived"
    IsApproved = "IsApproved"

    MENTOREMAIL = "Email_mentor"
    MENTORNAME = "Name_mentor"
    MENTORORG = "Name Of Organization"
    MENTOR_TITLE="Title_mentor"
    MENTOR_ADD = "Company Address"

    StudentFName = "First Name"
    StudentLName = "Last Name"
    StudentEmail = "Email"
    StudentFullNameLower = "StudentFLower"

    INTERNSHIP_START_DATE = "Internship Start Date"

    # tracker
    StudentName = "Student"
    ActivityPlan = "Internship Activity Plan"


    @staticmethod
    def ToList():
        return [ColNames.IsApproved, ColNames.MentorMailSentOn,ColNames.MentorLOAReceived ]
