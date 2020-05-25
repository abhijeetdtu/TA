import json
import pathlib
import os
import re

path = pathlib.Path().resolve()
jsFile = os.path.abspath(os.path.join(path , "TA" , "Linkedin" , "results_to_clea.json"))

fp  = open(jsFile , "r" , encoding="utf8")
#js = json.load(fp)

text = fp.read()
results  = re.findall('employment\': \[(.+)\]' , text)

rs = []
for r in results:
    ras = [ra.split("', '") for ra in r.split('", "')]
    rs.append(ras)
