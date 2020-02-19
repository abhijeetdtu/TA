import gspread
import gspread_dataframe as gd

from oauth2client.service_account import ServiceAccountCredentials

from email.utils import parseaddr

import os
import json
import pandas as pd

from TA.Email.Emailer import SendEmail
from TA.Sheets.utils import PrintWithPad , ColNames
from TA.Conf import Config


class GetSheets:



    def __init__(self , pathToCreds =None):
        scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

        path = pathToCreds if pathToCreds is not None else self.GetPath()
        creds = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
        client = gspread.authorize(creds)
        self.client = client

        newCols = ColNames.ToList()

        self.newCols = {}
        for i,col in enumerate(newCols):
            cola = chr(ord("A") + i)
            self.newCols[col] = {
                "coli" : i+1,
                "cola" : cola
            }



    def GetPath(self):
        return os.path.abspath(os.path.join(os.path.dirname(__file__) , ".." , "Creds" , "client_secret.json"))


    def Open(self,url):
        doc = self.client.open_by_url(url)
        s = doc.sheet1
        self.doc  = doc
        self.sheet = s
        return doc

    def OpenAsDF(self , url , sheet=None):
        doc = self.Open(url)
        if sheet == None:
            return self.ToDataFrame(doc.sheet1)


    def ToDataFrame(self ,sheet ):
        li = sheet.get_all_values()
        cols = li[0]
        #print(list)
        #df = pd.read_json(json.dumps(list) , orient="records" )
        df = pd.DataFrame(li[1:] , columns = li[0])
        df.columns = ["IsApproved"] + list(cols[1:-7]) + list([c+"_mentor" for c in  cols[-7:-3]]) + list(cols[-3:])
        print(df.columns)
        print(df.head())
        return df

    def CountPendings(self,df):
        PrintWithPad("Approvals - ")

        print(df["IsApproved"].value_counts())

        PrintWithPad("People Not Approved Yet - ")
        notapproveds = df[~df["IsApproved"].isin(["Approved" , "approved"])]
        colselect = ["IsApproved" , "First Name" , "Last Name"]
        print(notapproveds[colselect])

    def CountMailsPending(self,df):
        print(df[df[ColNames.MentorMailSentOn] == ""][[ColNames.StudentFName , ColNames.StudentLName ,ColNames.IsApproved]])

    def ForDupCreateColumns(self, wsheet , ssheet):
        requests = []

        requests.append({
              "insertDimension": {
                "range": {
                  "sheetId": wsheet.id,
                  "dimension": "COLUMNS",
                  "startIndex": 1,
                  "endIndex": 3
                },
                "inheritFromBefore": True
              }
            })

        body = {
            'requests': requests
        }

        ssheet.batch_update(body)
        for col , vals in self.newCols.items():
            wsheet.update_acell('{}1'.format(vals["cola"]), col)

    def CreateDupIfNotAlready(self , doc , sheet):
        title = "Dup_Copy"
        dup = [w  for w in doc.worksheets() if w.title == title]
        if len(dup) == 0 :
            print("ready to insert")
            self.dup = doc.duplicate_sheet(sheet.id , new_sheet_name=title )
            self.ForDupCreateColumns(self.dup , doc)
        else:
            self.dup = dup[0]

    def SendMentorMails(self , dup,df):
        print("Mail should be sent to these-")
        df = df[df[ColNames.IsApproved].isin(["Approved" , "approved"])]
        #print(df[df[ColNames.MentorMailSentOn] == ""][[ColNames.MENTORNAME , ColNames.MENTOREMAIL]])
        infoCols = [ColNames.StudentFName,ColNames.StudentLName ,ColNames.MENTORORG , ColNames.MENTOR_TITLE , ColNames.MENTOR_ADD , ColNames.MENTORNAME , ColNames.MENTOREMAIL]
        needtoSend = df[df[ColNames.MentorMailSentOn] == ""][infoCols]
        needtoSend[ColNames.MENTOREMAIL] = needtoSend[ColNames.MENTOREMAIL].apply(lambda x: parseaddr(x)[-1])
        print("Need to mail - {}".format(needtoSend.shape[0]))
        for row in json.loads(needtoSend.to_json(orient="records")):
            SendEmail(row)



    def Run(self):
        doc = self.Open()
        self.CreateDupIfNotAlready(self.doc , self.sheet)
        df = self.ToDataFrame(self.dup)
        #self.CountPendings(df)
        #self.SendMentorMails(self.dup,df)
        self.CountMailsPending(df)

    def CleanSheets(self,df):
        df.dropna(inplace=True , how="all")

    def StripPhone(self,phone):
        phone = str(phone)
        for char in "() -":
            phone = phone.replace(char , "")
        return phone

    def StudentsLOAReceived(self,dfsot , dfment):
        sdf = dfsot.loc[(dfsot["sfname"].isin(dfment["sfname"])) & (~dfsot[ColNames.MentorMailSentOn].isna())]
        sdunm = dfsot.loc[(dfsot["sfname"].isin(dfment["sfname"])) & (~dfsot[ColNames.MentorMailSentOn].isna()) & (dfsot[ColNames.MentorLOAReceived].isna())]
        print("-------- LOA Recieved {}-------------\n\n".format(sdf.shape[0]))
        print(sdf[["sfname" , "Email.1" , "Phone"] ].sort_values(["sfname"]) )
        print("\n\n-------- END-------------\n\n")

        print("-------- LOA Form Recieved But Still UnMakred {}----------\n\n".format(sdunm.shape[0]))
        print(sdunm[["sfname" , "Email.1" , "Phone"] ].sort_values(["sfname"]) )
        print("\n\n-------- END-------------\n\n")

        return sdf,"StudentsLOAReceived"

    def LOAReceivedMismatch(self,dfsot , dfment):
        sdf = dfment.loc[~dfment["sfname"].isin(dfsot["sfname"])]
        print("-------- LOA Recieved {} BUT not found in Student Form-------------\n\n".format(sdf.shape[0]))
        print(sdf[["sfname" , "Name" , "Email" , "Phone"] ].sort_values(["sfname" , "Name"]) )
        print("\n\n-------- END-------------\n\n")
        return sdf,"LOAReceivedMismatch"

    def MailSentNoResponseYet(self,dfsot,dfment):
        sdf = dfsot.loc[(~dfsot["MentorMailSentOn"].isna()) & (~dfsot["sfname"].isin(dfment["sfname"]))]
        print("-------- LOA Sent but Not Recieved {}-------------\n\n".format(sdf.shape[0]))
        print(sdf[["sfname" , "Email.1" , "Phone"] ].sort_values(["sfname"]) )
        print("\n\n-------- END-------------\n\n")
        return sdf,"MailSentNoResponseYet"

    def CrossCheckResponses(self , studentSOTURL , mentorResponseURL):
        asdf = gd.get_as_dataframe
        sots = self.Open(studentSOTURL).sheet1
        ments = self.Open(mentorResponseURL).sheet1
        dfsot = asdf(sots)
        dfment = asdf(ments)
        dfment.dropna(inplace=True , how="all")
        dfsot.dropna(inplace=True , how="all")

        dfment["sfname"] = dfment["Student Name"].str.lower().str.strip(" ")
        dfsot["sfname"] = dfsot["First Name"].str.strip(" ") + " " + dfsot["Last Name"].str.strip(" ")
        dfsot["sfname"] = dfsot["sfname"].str.lower().str.strip(" ")
        #dfsot.to_csv("./test.csv")
        #dfment.to_csv("./test2.csv")
        #dfsot.loc[(dfsot["FullName"].isin(dfment["sname"])) & (~dfsot["MentorMailSentOn"].isna()) ,["MentorLOAReceived"]] = "01/22/20"
        #print(dfsot["Phone.1"].sort_values().unique())
        resp = [func(dfsot,dfment) for func in [self.StudentsLOAReceived,
                     self.LOAReceivedMismatch,
                     self.MailSentNoResponseYet
                    ]]

        total = sum([df.shape[0] for df,t in resp])

        for x,y in resp:
            print(y + " : " + str(x.shape[0]) + "\n")
        print("\n\nTotal Unaccounted for = {} Rows(could be duplicate or double check MailSentNoResponseYet List). Please Check Mails for Docx responses".format(dfsot.shape[0] - total))


        #print(dfsot[dfsot["MentorLOAReceived"] == "01/22/20"].shape)

        #gd.set_with_dataframe()
        #dfment["fullname"] = dfment["fir"]



if __name__ == "__main__":
    GetSheets().Run()
    #GetSheets().CrossCheckResponses(Config.studentSOTURL,Config.mentorResponseURL)
