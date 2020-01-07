import requests
from conllu import parse_tree
import pickle
import matplotlib.pylab as plt
from stop_words import get_stop_words
import time
import os


stopwords = get_stop_words("fi")

poslist = []
verblist = []
nounlist = []

posall = []
verball = []
nounall = []

headers = {
    'Content-Type': 'text/plain; charset=utf-8',
}


def startTree(treeStart):
    tokeni = treeStart.token
    if tokeni['upostag'] == "VERB":
        #Root = predicate
        verblist.append(tokeni['lemma'].lower())
        rootkids = treeStart.children
        for kid in rootkids:
            kidtoken = kid.token
            goTree(kid, treeStart)
    else:
        #copular clause
        goTree(treeStart, treeStart)
        
def goTree(tree, treeStart):
    tokeni = tree.token
    #print(tokeni)
    compounds = tokeni['lemma'].split("#")
    for word in compounds:
        if word.lower() == "brexi" or word.lower() == "brexit" or word.lower() == "brexitti" or word.lower() == "brex":
            #we found the brexit node, is it the head of the noun phrase?
            poslist.append(tokeni['upostag'])
            dep = tokeni['deprel']
            if dep.startswith("nsubj") or dep.startswith("obj") or dep.startswith("obl") or dep.startswith("root"):
                #the head of NP
                nounPhraseTree(tree, 0)
            else:
                #print("HEAD ID: " + str(tokeni['head']))
                headtree = findNPHead(tokeni['head'], treeStart, treeStart)
                #print(headtree)
                nounPhraseTree(headtree, 0)
    kids = tree.children
    if len(kids) > 0:
        for kid in kids:
            goTree(kid, treeStart)
            
def findNPHead(nodeid, tree, ogtree):
    tokeni = tree.token
    if tokeni['id'] == nodeid:
        dep = tokeni['deprel']
        if dep.startswith("nsubj") or dep.startswith("obj") or dep.startswith("obl") or dep.startswith("root"):
            #the head of NP
            return tree
        else:
            newtarget = tokeni['head']
            return findNPHead(newtarget, ogtree, ogtree)
    else:
        kids = tree.children
        for kid in kids:
            possiblehead = findNPHead(nodeid, kid, ogtree)
            #print(possiblehead)
            try:
                possiblehead.token
                return possiblehead
            except AttributeError:
                continue
        return 0
    
            
def nounPhraseTree(tree, depth):
    tokeni = tree.token
    compounds = tokeni['lemma'].split("#")
    for word in compounds:
        if word.lower() == "brexi" or word.lower() == "brexit" or word.lower() == "brexitti" or word.lower() == "brex":
            #this is the brexit node, irrelevant for context
            pass
        else:
            dep = tokeni['deprel']
            if dep.startswith("amod") or dep.startswith("nmod") or dep.startswith("acl") or dep.startswith("det") or dep.startswith("nummod") or dep.startswith("appos") or dep.startswith("case") or dep.startswith("conj") or dep.startswith("cc") or dep.startswith("advmod") or dep.startswith("advcl"):
                nounlist.append(word.lower())
            elif depth == 0:
                if dep.startswith("nsubj"):
                    nounlist.append(word.lower())
    kids = tree.children
    if len(kids) > 0:
        for kid in kids:
            nounPhraseTree(kid, depth + 1)
    

starttime = time.time()
sents = dict()
with open('organizedsent.pckl', 'rb') as f:
    sents = pickle.load(f)
    f.close()
    
#Test if dir for some reason doesn't exist
try:
    # Create target Directory
    os.mkdir("tnparserimages")
except FileExistsError:
    pass

def sentToServer(sentences, month):
    data = '. '.join(sent for sent in sentences)
    data = data.encode("utf-8")

    response = requests.post('http://localhost:7689/', headers=headers, data=data)
    response.encoding = 'utf-8'
    #print(response.text)
    poslist[:] = []
    verblist[:] = []
    nounlist[:] = []
    for tokentree in parse_tree(response.text):
        #tokentree.print_tree()
        startTree(tokentree)
    
    posall.extend(poslist)
    verball.extend(verblist)
    nounall.extend(nounlist)
    
    counts = dict()
    for i in poslist:
        counts[i] = counts.get(i, 0) + 1

    counts2 = dict()
    for i in verblist:
        if i in stopwords:
            continue
        else:
            counts2[i] = counts2.get(i, 0) + 1

    counts3 = dict()
    for i in nounlist:
        if i in stopwords:
            continue
        else:
            counts3[i] = counts3.get(i, 0) + 1
        
    postags = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    nounss = sorted(counts3.items(), key=lambda x: x[1], reverse=True)
    verbss = sorted(counts2.items(), key=lambda x: x[1], reverse=True)
    
    lab, amount = zip(*postags)
    plt.figure(figsize=(12, 9))
    plt.title(month + ' POS tags')
    plt.pie(amount, labels=lab, autopct='%1.1f%%')
    plt.savefig("tnparserimages/" + month + 'pos.png')
    plt.close()
    
    
    if len(nounss) > 0:
        nounss2 = nounss[:10]
        x, y = zip(*nounss2)
        plt.figure(figsize=(12, 9))
        plt.title(month + ' Noun Phrase')
        plt.bar(x,y)
        plt.savefig("tnparserimages/" + month + 'noun.png')
        plt.close()
    if len(verbss) > 0:
        verbss2 = verbss[:10]
        x2, y2 = zip(*verbss2)
        plt.figure(figsize=(12, 9))
        plt.title(month + ' Main Verb')
        plt.bar(x2,y2)
        plt.savefig("tnparserimages/" + month + 'verb.png')
        plt.close()
    
    
    #print(counts)
    #print(counts2)
    #print(counts3)
    
for key in sents:
    sentences = sents[key]
    print("Analysing sentences from " + str(key))
    sentToServer(sentences, key)
    
endtime = time.time() - starttime
print("Time spent analysing: " + str(endtime))
counts = dict()
for i in posall:
    counts[i] = counts.get(i, 0) + 1

counts2 = dict()
for i in verball:
    if i in stopwords:
        continue
    else:
        counts2[i] = counts2.get(i, 0) + 1

counts3 = dict()
for i in nounall:
    if i in stopwords:
        continue
    else:
        counts3[i] = counts3.get(i, 0) + 1
        
postags = sorted(counts.items(), key=lambda x: x[1], reverse=True)
nounss = sorted(counts3.items(), key=lambda x: x[1], reverse=True)
verbss = sorted(counts2.items(), key=lambda x: x[1], reverse=True)

lab, amount = zip(*postags)
plt.figure(figsize=(12, 9))
plt.title('POS tags')
plt.pie(amount, labels=lab, autopct='%1.1f%%')
plt.savefig('tnparserimages/allpos.png')
plt.show()


if len(nounss) > 0:
    nounss2 = nounss[:10]
    x, y = zip(*nounss2)
    plt.figure(figsize=(12, 9))
    plt.title('All Noun Phrases')
    plt.bar(x,y)
    plt.savefig('tnparserimages/allnoun.png')
    plt.show()
if len(verbss) > 0:
    verbss2 = verbss[:10]
    x2, y2 = zip(*verbss2)
    plt.figure(figsize=(12, 9))
    plt.title('All Main Verbs')
    plt.bar(x2,y2)
    plt.savefig('tnparserimages/allverb.png')
    plt.show()