import os
import sys
import smtplib, ssl

# Import the email modules we'll need
from email import encoders
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from TA.Sheets.utils import PrintWithPad
from TA.Sheets.utils import ColNames
from TA.Creds.emailconf import Conf

class EmailFormatter:

    def __init__(self , templateFile=None):
        self.templateFile = templateFile if templateFile is not None else self.GetTemplatePath()
        self.template = open(self.templateFile , "r").read()

    def GetTemplatePath(self):
        return os.path.abspath(os.path.join(os.path.dirname(__file__) , "Email.tml"))

    def GetEmailFormatted(self , info):
        return self.template.format(**info)


class Emailer:

    def __init__(self,email,password):
        context = ssl.create_default_context()
        self.server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
        self.server.login(email,password)
        # Open the plain text file whose name is in textfile for reading.


    def Send(self,subject , fromEmail ,toEmail,ccEmail, message , attachement):

        msg = MIMEMultipart()
        #msg.set_content(message)
        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = subject
        msg['From'] = fromEmail
        msg['To'] = toEmail
        msg["Cc"] = ccEmail
        msg.attach(MIMEText(message, "plain"))

        if attachement != None:
            attachPath = os.path.abspath(os.path.join(os.path.dirname(__file__) ,attachement) )
            msg = self.Attachment(attachPath , msg)

        print("\n\n------MAIL-----")
        print("TO {}".format(toEmail))
        print("FROM {}".format(fromEmail))
        print("CC {}".format(ccEmail))

        self.server.send_message(msg)
        
        print(message)
        # getInp = input("Send Mail (y/n) ?").lower()
        # if getInp == "exit":
        #     sys.exit()
        # if getInp == "y":
        #     self.server.send_message(msg)
        #     print("Sent message to - {}".format(toEmail))
        # else:
        #     print("Msg not sent")
        # print("------MAIL END----- {}".format(toEmail))
        return True

    def Attachment(self , filepath , message):
        with open(filepath, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {Conf.attachment}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)
            return message


def InfoObj(row):
    mentorTitle = row[ColNames.MENTOR_TITLE].strip(" ")
    if len(mentorTitle) > 50:
        mentorTitle =""
    info = {
        "mentor" : {
            "Title" : mentorTitle,
            "Org":row[ColNames.MENTORORG].strip(" "),
            "Address":row[ColNames.MENTOR_ADD],
            "FirstName" : row[ColNames.MENTORNAME]
        },
        "student" :  {
            "FirstName" : row[ColNames.StudentFName],
            "LastName" : row[ColNames.StudentLName]
        },
        "googleLink" : Conf.googleLink
    }

    return info

EmailerSingle = Emailer(Conf.fromEmail , Conf.password)

def SendEmail(infoRow):
    info = InfoObj(infoRow)
    toEmail = infoRow[ColNames.MENTOREMAIL]
    msg = EmailFormatter().GetEmailFormatted(info)
    EmailerSingle.Send( Conf.subject , Conf.fromEmail , toEmail ,Conf.ccEmail, msg , Conf.attachment)

if __name__ == "__main__":
    row = {'First Name': 'Sai Smaran', 'Last Name': 'Annamraju', 'Name Of Organization': 'UNC Charlotte, Department of Political Science and Public Administration', 'Title_mentor': 'Associate Director', 'Company Address': 'UNC Charlotte', 'Name_mentor': 'Jason Windett', 'Email_mentor': 'jwindett@uncc.edu'}
    SendEmail(row)
