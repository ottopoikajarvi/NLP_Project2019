import pickle
import plotSentenceLength as pltlen
import os
import sys


sentences = []

with open('yleSentences.pckl', 'rb') as f:
    sentences = pickle.load(f)
    f.close()

if len(sys.argv) == 2:
    print(sys.argv[1])

try:
    # Create target Directory
    os.mkdir("tnparserimages")
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