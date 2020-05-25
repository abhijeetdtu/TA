import pathlib
import os
import re

path = pathlib.Path().resolve()
pathToList = os.path.abspath(os.path.join("TA" , "Linkedin" , "alumni_list.txt"))

def getNamesFromDefaultTXT():
    return getNames(pathToList)
    
def getNames(pathToList):
    with open(pathToList , "r") as f:
        all= f.read()
        clean = re.subn("\t" , " " , all)[0]
        clean = re.subn("\w\." , "" , clean)[0]
        clean = re.subn(" +" , " " , clean)[0]
        items = [c.strip(" ") for c in clean.split("\n") if c != '' and len(c.split(" ")) < 3]
        return items
