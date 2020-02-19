import os
import pathlib

from TA.TextAnalytics.NLTK import SentencesToPOSHTML,Summa
from TA.TextAnalytics.PltToImg import ToHTMLImg,ToHTML
from pdfminer.high_level import extract_text


from wordcloud import WordCloud

path  =pathlib.Path().resolve()

pathToFiles = os.path.abspath(os.path.join(path , "TA" , "Sheets" , "_tempWorkspace" , "118638" , "Internship Activity Plan"))
outFile = os.path.abspath(os.path.join(os.path.dirname(__file__) , "Output.html"))


def AnalyseFiles(pathToFiles):
    allSents = []
    for f in os.listdir(pathToFiles):
        print(f)
        if f.find(".pdf") > 0:
            p = os.path.abspath(os.path.join(pathToFiles  ,f))
            txt =extract_text(p)
            sents= Summa(txt)
            cloud = WordCloud(width=480, height=480, margin=0).generate(txt)
            img = cloud.to_image()
            img = ToHTMLImg(img)
            fileResults = (f, sents,img)
            allSents.append(fileResults)
    return allSents


def SentsToHTML(allSents):

    with open(outFile , "w" , encoding="utf8") as of:
        #body = "\n".join(allSents)
        body = [ToHTML(f,SentencesToPOSHTML(sents),img) for f,sents,img in allSents ]
        body = "".join(body)

        html = """
            <html>
                <head>
                    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
                </head>
                <body>
                    <div class="container">
                        {}
                    </div>
                </body>
            </html>
        """

        of.write(html.format(body))



def Run(pathToFiles):
    sents = AnalyseFiles(pathToFiles)
    SentsToHTML(sents)

if __name__ == "__main__":
    pathToFiles = "C:/Users/Abhijeet/Documents/GitHub/TA/TA/Sheets/_tempWorkspace/Internship/Progress Report 1"
    # Path = ""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--path-to-folder" , default=pathToFiles)

    args = parser.parse_args()

    #print(args.path_to_folder)
    Run(args.path_to_folder)
#from sklearn.feature_extraction.text import TfidfVectorizer
