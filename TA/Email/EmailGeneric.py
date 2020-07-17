from TA.Email.Emailer import EmailerSingle
from TA.Email.Emailer import EmailFormatter

import json
import os
import argparse

class EmailerGeneric:

    def __init__(self , pathConfigJsonOrName , isDryRun):

        self.config = self._getConfig(pathConfigJsonOrName)
        self.template_path = self.config["template_path"]
        self.emailer = EmailerSingle
        self.isDryRun = isDryRun

    def _getConfig(self, pathConfigJsonOrName):
        baseConfigPath = os.path.abspath(os.path.join(os.path.dirname(__file__) , "config.json"))
        conf = json.load(open(baseConfigPath, "r"))

        if os.path.exists(pathConfigJsonOrName):
            path = pathConfigJsonOrName
        elif pathConfigJsonOrName in conf:
            path = conf[pathConfigJsonOrName]
        else:
            raise("Path doesn't exist or Name not mentioned in config.json")

        return json.load(open(path, "r"))

    def Run(self):
        subject = self.config["mail_subject"]
        fromEmail =   self.config["from"]
        ccEmail =   ", ".join(self.config["cc"])
        attachment = self.config["global"]["doc_link"]

        for r in self.config["recipients"]:
            #email = r["Email"]
            #print(self.config["global"])
            for k,v in self.config["global"].items():
                r[k]=v
            #toEmail = fromEmail
            toEmail = r["Email"] if not self.isDryRun else fromEmail
            msg = EmailFormatter(self.template_path).GetEmailFormatted(r)
            print(f"\n\n{msg}\n" , toEmail)
            self.emailer.Send(subject , fromEmail ,toEmail , ccEmail,msg, attachment )


if __name__ == "__main__":
    """
    
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--pathOrName" , help="path to Email config.json or name/key mentioned config.json")
    parser.add_argument("--isDryRun" ,default="Yes" , help="Yes or No - Whether to actually send out emails to recipients or back to the sender. Yes - back to sender. No - to recpient mentioned in config")

    args = parser.parse_args()
    EmailerGeneric(args.pathOrName, args.isDryRun.lower() == "yes").Run()
