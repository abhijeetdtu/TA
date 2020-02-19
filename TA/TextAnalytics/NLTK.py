import nltk

#nltk.download("averaged_perceptron_tagger")
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# text = """Current Tasks:
# My project will be within the Human Resources (HR) group in WestRock company. The first two weeks of
# the internship are focused on orientation and organizational understanding. Task 1 of the week is to
# meet and greet Human Resources leadership. Task 2 is the understand the HR organizational structure.
# Task 3 is to understand the different HR systems and the uses of each systems. Task 4 is to job shadow
# an experienced coworker. Task 5 to get access to the different HR systems that will be needed for the
# internship.
# """
# sentences = Summa(text)

def Summa(text):
    LANGUAGE = "english"
    SENTENCES_COUNT = 10
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    sentences = [str(sent).replace("\t" , " ") for sent in summarizer(parser.document, SENTENCES_COUNT)]
    return list(sentences)

def POSToHTML(sentence):
    words = []
    colorMap = {
        "NNP" : "purple"
        ,"NNPS": "blue"
        ,"NN" :"red"
    }
    for word,pos in sentence:
        print(word,pos)
        if pos in ["NNP" , "NNPS"  , "NN"]:
            words.append( "<span style='color:{};'> <b>{} </b> </span>".format(colorMap[pos],word))
        else:
            words.append(word)
    return " ".join(words)

def SentencesToPOSHTML(sentences):
    print(f"Tokenizing - {len(sentences)} sentences")
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    print("POS Tagging")
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return [ POSToHTML(sent) for sent in sentences]
