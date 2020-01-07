import pickle

sentences = []

with open('yleSentences.pckl', 'rb') as f:
    sentences = pickle.load(f)
    f.close()

datedict = dict()
for i in sentences:
    date = i[0]
    if date in datedict:
        datedict[date].append(i[3])
    else:
        datedict[date] = [i[3]]
        
print(datedict.keys())

with open('organizedsent.pckl', 'wb') as f:
    pickle.dump(datedict, f)