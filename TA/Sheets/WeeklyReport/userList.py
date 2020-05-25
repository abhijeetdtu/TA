from TA.Login.Login import Login
from TA.Sheets.WeeklyReport.apiEndpoints import ENDPOINTS
import json

class CourseUsers:

    def __init__(self,courseId):
        self.courseId = courseId
        self.url = ENDPOINTS.USERS_LIST.format(**{"COURSE_ID" : courseId})

    def getList(self):
        resp = Login.StaticAuthGet(self.url)
        text = resp.text
        text = text.replace("while(1);","")
        js = json.loads(text)
        return js

    def getOnlyBasics(self):
        js = self.getList()
        return [ (user["id"] ,user["name"] ,user["created_at"] , user["email"] , user["loginid"]) for user in js]



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--course-id")

    args = parser.parse_args()

    ca = CourseUsers(args.course_id)
    an = ca.getList()
    print(an)
    json.dump(an,open("_delete.json" , "w") )
