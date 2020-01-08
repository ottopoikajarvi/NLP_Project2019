import pickle
import plotSentenceLength as pltlen
import os
import sys
from nltk.stem.snowball import FinnishStemmer
import subprocess

origsentences = []
sentences = []

with open('yleSentences.pckl', 'rb') as f:
    origsentences = pickle.load(f)
    f.close()

if len(sys.argv) == 2:
    print("Looking for sentences with " + str(sys.argv[1]))
    stemmer = FinnishStemmer()
    stemarg = stemmer.stem(sys.argv[1])
    print("Stem: " + stemarg)
    for sent in origsentences:
        words = sent[6]
        for word in words:
            if word.startswith(stemarg):
                sentences.append(sent)
else:
    sentences = origsententes
    
print("Found " + str(len(sentences)) + " sentences")
if len(sentences) == 0:
    exit()

try:
    # Create target Directory
    os.mkdir("tnparserimages")
    print("Directory ./tnparserimages created")
except FileExistsError:
    pass

print("Sentence lengths...")
pltlen.plotSentenceLength(sentences)
    
datedict = dict()
for i in sentences:
    date = i[0]
    if date in datedict:
        datedict[date].append(i[3])
    else:
        datedict[date] = [i[3]]
        
#print(datedict.keys())

with open('organizedsent.pckl', 'wb') as f:
    pickle.dump(datedict, f)
    
print("Dictionary for tnparser_wrap created\nStarting parsing")

subprocess.Popen("python3 tnparser_wrap.py", shell=True)