from TA.Email.Emailer import EmailerSingle
from TA.Email.Emailer import EmailFormatter

import json
import os
import argparse

class EmailerGeneric:

    def __init__(self , pathConfigJsonOrName):

        self.config = self._getConfig(pathConfigJsonOrName)
        self.template_path = self.config["template_path"]
        self.emailer = EmailerSingle

    def _getConfig(self, pathConfigJsonOrName):
        baseConfigPath = os.path.abspath(os.path.join(os.path.dirname(__file__) , "config.json"))
        conf = json.load(open(baseConfigPath, "r"))

        if os.path.exists(pathConfigJsonOrName):
            path = pathConfigJson
        elif pathConfigJsonOrName in conf:
            path = conf[pathConfigJsonOrName]
        else:
            raise("Path doesn't exist or Name not mentioned in config.json")

        return json.load(open(path, "r"))

    def Run(self):
        subject = self.config["mail_subject"]
        fromEmail =   self.config["from"]
        ccEmail =   ", ".join(self.config["cc"])

        for r in self.config["recipients"]:
            #email = r["Email"]
            toEmail = fromEmail
            msg = EmailFormatter(self.template_path).GetEmailFormatted(r)
            print(f"\n\n{msg}\n")
            self.emailer.Send(subject , fromEmail ,toEmail , ccEmail,msg, None )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pathOrName" , help="path to Email config.json or name/key mentioned config.json")

    args = parser.parse_args()
    EmailerGeneric(args.pathOrName).Run()
