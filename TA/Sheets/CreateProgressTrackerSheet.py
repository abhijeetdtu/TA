from TA.Sheets.GetSheet import GetSheets
from TA.Conf import Config
from TA.Sheets.utils import ColNames , CanvasURLS
from TA.Login.Login import Login
from TA.Sheets.utils import DumpVersionedDF

from collections import defaultdict

import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import os
import shutil
from fuzzywuzzy import fuzz
import datetime
import argparse



class ProgressTracker:

    class Status:
        DONE = "Done"
        NOT_DONE = "Not Done"

    def __init__(self):
        gs = GetSheets()
        # Make sure you have access to STUDENT SOT URL SHEET
        self.studentSOT = gs.OpenAsDF(Config.studentSOTURL)
        self.studentSOT[ColNames.StudentFullNameLower] = self.GetStudentNames()
        self.studentSOT[ColNames.StudentFullNameLower] = self.studentSOT[ColNames.StudentFullNameLower].str.lower()
        self.studentSOT[ColNames.INTERNSHIP_START_DATE] = pd.to_datetime(self.studentSOT[ColNames.INTERNSHIP_START_DATE] , format="%m/%d/%Y")
        self.workspace = os.path.abspath(os.path.join(os.path.dirname(__file__) , "_tempWorkspace"))
        self.outputTrackerName = "Tracker.xlsx"

    def GetSubmissionDownloadUrl(self , u):
        return u + "/submissions?zip=1"

    def _GetAssignmentList(self):
        return ["ActivityPlan" ] + [f"ProgressReport{i}" for i in range(1,7)] + ["FinalPresentation" , "PeerReviews" , "FinalReport"]

    def PathToAssignmentFolder(self , assignment):
        return os.path.abspath(os.path.join(self.workspace ,assignment))

    def DownloadAssignments(self, urls , texts):
        urls = [ self.GetSubmissionDownloadUrl(u) for u in urls]
        for i,u in enumerate(urls):
            p = self.PathToAssignmentFolder(texts[i])
            print(f"Downloading - {u}")
            Login.DownloadZIP(u , p )

    def GetAssignmentList(self, url=None):
        url = Config.courseAssignmentURL if url == None else url

        # Make sure you have access to the internship course in Canvas
        # Also to have signed in the firefox browser
        text = Login.GetUrl(url ,"a.element_toggler.accessible-toggler")
        #print(text)
        soup = BeautifulSoup(text)
        a = soup.findAll("a" , attrs={"class" : "ig-title"})
        texts = [elm.text.strip(" \n") for elm in a]
        urls = [elem.attrs["href"] for elem in a]
        return texts,urls

    def GetExportFilePath(self):
        return os.path.abspath(os.path.join(self.workspace, self.outputTrackerName))

    def GetStudentNames(self):
        return list(self.studentSOT[ColNames.StudentFName] + " " + self.studentSOT[ColNames.StudentLName])

    def GetStudentNamesFromDF(self,df):
        return list(df[ColNames.StudentFName] + " " + df[ColNames.StudentLName])

    def MatchStudentNamesToNinerIds(self, snames , ninerIds):
        match = {}
        matchInv = {}
        for id in ninerIds:
            id = id.lower()
            maxmatch = -1
            if id in Config.CORRECTIONS["NINERIDS"]:
                n =  Config.CORRECTIONS["NINERIDS"][id]
                match[id] = n
                matchInv[n] = id
            else:
                for sname in snames:
                    snameLower = sname.lower()
                    ratio = fuzz.ratio(snameLower , id)
                    if ratio > maxmatch:
                        match[id] = sname
                        #match[sname] = id
                        maxmatch = ratio

        for k,v in match.items():
            matchInv[v] = k
        return match.values() , matchInv

    def CreateDF(self,jsonObj):
        df = pd.read_json(json.dumps(jsonObj) , orient="records")
        df["Student"] = list(df.index)
        df.to_excel(self.GetExportFilePath())
        return df

    def CreateWorkspace(self ,id=None):
        if id != None:
            self.workspace = os.path.abspath(os.path.join(self.workspace , id))
        if os.path.exists(self.workspace):
            shutil.rmtree(self.workspace)
        os.mkdir(self.workspace)

    def GetWhoDidIt(self , assignment):
        ids = []
        p = self.PathToAssignmentFolder(assignment)
        if os.path.exists(p):
            for f in os.listdir(self.PathToAssignmentFolder(assignment)):
                ninerId = f.split("_")[0]
                ids.append(ninerId)
        return ids

    def CaptureStudentWork(self ,text, studentNames , ninerIds , students):
        matched,minv = self.MatchStudentNamesToNinerIds(studentNames ,ninerIds)
        for m in matched:
            students[text][m] = ProgressTracker.Status.DONE
            students["CanvasId"][m] = minv[m]#str(datetime.date.today().isoformat())
        for s in studentNames:
            if s not in matched:
                students[text][s] = ProgressTracker.Status.NOT_DONE
        return students

    def PrepareWhoDidItForAllAssignments(self,assignments , studentNames):
        students = defaultdict(dict)
        for text in assignments:
            ninerIds = self.GetWhoDidIt(text)
            if studentNames == None:
                for id in ninerIds:
                    students[text][id] =  ProgressTracker.Status.DONE
            else:
                students = self.CaptureStudentWork(text,studentNames , ninerIds , students)

        return students

    def DidStudentDoIt(self,whodidits ,assignment, student):
        return student in whodidits[assignment]

    def PrepareWhoDidItJson(self ,whodidits,assignments, df):
        for i,row in df.iterrows():
            #print(row)
            label,data = row
            student = row["Student"]
            for c in row:
                if c != "Student":
                    print(student,c)

    def DumpDF(self,df):
        DumpVersionedDF(self.outputTrackerName,df , ColNames.StudentFName)

    def Run(self):
        self.CreateWorkspace("Internship")
        studentNames = self.GetStudentNames()
        texts , urls = self.GetAssignmentList()
        self.DownloadAssignments(urls , texts)
        whoDidIts = self.PrepareWhoDidItForAllAssignments(texts , studentNames)
        df = self.CreateDF(whoDidIts)
        self.Validate(df)
        #self.DumpDF(df)

    def Validate(self , df):
        self.ValidateActivityPlanSubmission(df)

    def ValidateActivityPlanSubmission(self,df):
        trackerNotDone = df[df[ColNames.ActivityPlan] == ProgressTracker.Status.NOT_DONE]
        startedIndex = self.studentSOT[ColNames.INTERNSHIP_START_DATE] < (datetime.datetime.today() - datetime.timedelta(days = 14))
        internStarted = self.studentSOT[startedIndex]
        internNotStarted = self.studentSOT[~startedIndex]

        internStarted["Student"] = self.GetStudentNamesFromDF(internStarted)
        internStarted["Student"] = internStarted["Student"].str.lower()
        trackerNotDone["Student"] = trackerNotDone["Student"].str.lower()

        cdf = pd.merge(internStarted , trackerNotDone , on="Student")
        cdf = cdf.drop_duplicates()

        #print(trackerNotDone.columns)
        print(f"\n\n--------------Students with activity plan not turned in - {trackerNotDone.shape[0]}-------")
        print(trackerNotDone[["Student"]].drop_duplicates())
        print("END--------------Students with activity plan not turned in-------END\n\n")


        print(f"\n\n--------------Students Whos Intern started but activity plan not turned in - {cdf.shape[0]}-------")
        print(cdf[[ColNames.StudentFName , ColNames.StudentLName , ColNames.StudentEmail]])
        print("END--------------Students Whos Intern started but activity plan not turned in-------END\n\n")

        print(f"\n\n--------------Students Whos Intern Not started or Plan not due - {internNotStarted.shape[0]}-------")
        print(internNotStarted[[ColNames.StudentFName , ColNames.StudentLName , ColNames.StudentEmail , ColNames.INTERNSHIP_START_DATE , ColNames.IsApproved]].sort_values(ColNames.INTERNSHIP_START_DATE))
        print("END--------------Students Whos Intern NOt started -------END\n\n")

        print("------------------ Copy Json From Here--------------\n\n")
        cdf[ColNames.INTERNSHIP_START_DATE] = cdf[ColNames.INTERNSHIP_START_DATE].dt.strftime("%m-%d-%y")
        cdf = cdf[[ColNames.StudentFName , ColNames.StudentLName , ColNames.StudentEmail , ColNames.INTERNSHIP_START_DATE]]
        cdf = cdf.drop_duplicates()
        print(cdf.to_json(orient="records"))


    def StandAloneAssignmentCheck(self , courseId):
        url = CanvasURLS.GetCourseAssignmentURL(courseId)
        self.CreateWorkspace(courseId)
        texts , urls = self.GetAssignmentList(url)
        self.DownloadAssignments(urls , texts)
        whoDidIts = self.PrepareWhoDidItForAllAssignments(texts , None)
        df = self.CreateDF(whoDidIts)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--id",help="Id of the course for which to grab assignments")
    parser.add_argument("--sa")
    #ProgressTracker().Run()
    args = parser.parse_args()
    pt = ProgressTracker()

    if args.id == None:
        pt.Run()
    else:
        pt.StandAloneAssignmentCheck(args.id)


    # Python online 87897
    # Internship course 118638
    #pt.MatchStudentNamesToNinerIds(None  , pt.GetWhoDidIt("Internship Activity Plan"))
