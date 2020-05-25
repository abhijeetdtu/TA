from TA.Login.Login import Login
from TA.Sheets.WeeklyReport.apiEndpoints import ENDPOINTS
import json

class CourseAssignments:

    def __init__(self,courseId):
        self.courseId = courseId
        self.assignmentUrl = ENDPOINTS.ASSIGNEMENTS.format(**{"COURSE_ID" : courseId})

    def getAssignmentsList(self):
        NAME = "name"
        ID = "id"
        ASSIGNMENTS = "assignments"

        resp = Login.StaticAuthGet(self.assignmentUrl)
        text = resp.text
        text = text.replace("while(1);","")
        js = json.loads(text)

        assignments = []
        for group in js:
            gname= group[NAME]
            gid = group[ID]
            for assignment in group[ASSIGNMENTS]:
                aname = assignment[NAME]
                aid = assignment[ID]

                assignments.append([gname , gid , aname ,aid])

        return assignments

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--course-id")

    args = parser.parse_args()

    ca = CourseAssignments(args.course_id)
    an = ca.getAssignmentsList()
    print(an)
    #json.dump(an,open("_delete.json" , "w") )
