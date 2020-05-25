import pandas as pd
import os
import json

def toConfig(path , csv_name , mail_subject , mail_from,mail_cc):
    df = pd.read_csv(os.path.abspath(os.path.join(path , csv_name))) #, sep="\t")
    print(df.columns)
    df["student_name"] = df["First Name"] + " " + df["Last Name"]
    df["mentor"] = df["Name"]

    df = df.drop(["First Name" , "Last Name" , "Name"] , axis=1)
    df.head()
    config = {}

    config["recipients"] = json.loads(df.to_json(orient="records"))
    config["mail_subject"] = mail_subject
    config["from"] = mail_from
    config["cc"] = mail_cc
    return config

if __name__ == "__main__":
    path = "C:/Users/Abhijeet/Documents/GitHub/TA/TA/Email/Configs/Eval/"
    csv= "studentmentor.csv"

    ### Format for the csv - Can be copied from the internship proposal google sheet
    ## First Name,Last Name,Name,Email
    ## Alexander,Gulley,Aimee Marva,aimee.marva@ally.com
    ## Anjali,Bapat,Chris Sunde,chris@goodroads.io

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-folder" , default=path , help="Path to folder where source csv is and Where the config will be created")
    parser.add_argument("--csv-name" , default=csv , help="Name of the CSV with Student and Mentor Details")
    parser.add_argument("--mail-subject" , default="" , help="Subject of the Email to be sent")
    parser.add_argument("--frm" , default="" , help="Email address from which to send emails")
    parser.add_argument("--cc" , default=[] , help="List of Email addresses to cc in the email")

    args = parser.parse_args()

    config = toConfig(args.config_folder , args.csv_name , args.mail_subject,args.frm , args.cc)

    f = os.path.abspath(os.path.join(args.config_folder , "config.json"))
    json.dump( config , open(f , "w") )
    print(config)
