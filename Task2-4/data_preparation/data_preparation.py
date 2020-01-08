
def searchData(word):

    # Init
    import os

    # Search for senteces with 'brexit'
    root='./ylenews-fi-2011-2018-src/data/fi'
    ynames= os.listdir (root) 

    hits=[]

    for yname in ynames:
        mnames=os.listdir(os.path.join(root, yname))
        for mname in mnames:
            fnames=os.listdir(os.path.join(root, yname, mname))
            for fname in fnames:
                file00=open(os.path.join(root, yname, mname,fname),mode='r',encoding='UTF-8')
                contents=file00.read()
                contents=contents.split('\n')
                for i in contents:
                    res0=i.lower().find(word.lower())
                    if res0>-1:
                        hit=[os.path.join(root, yname, mname,fname),i]
                        hits.append(hit)
                file00.close()


    return hits


def parseSentences(hits, searchwords):
    # NLTK
    import nltk

    # Käydään läpi tulokset, splitataan lauseet, turhat merkit pois, tokenization
    import re

    sentences=[]
    for i in hits:
        if i[1].find('text')>-1:
            t00=i[0].split('/')
            year=t00[4]
            month=t00[5]

            clean=i[1].replace(' – ','').strip()
            clean=clean[8:]

            # Remove urls
            clean=re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', clean)

            # Remove 
            clean=re.sub(r'''[^a-zA-Z0-9?!. äÄöÖåÅ]''',' ',clean)
            clean=re.sub(' +', ' ',clean)

            #sent=clean.split('.')
            #sent=re.findall(r"[\w']+", clean)
            sent=nltk.sent_tokenize(clean)
            for j in sent:
                sent0=j.strip()
                origsent=sent0
                sent0=sent0.lower()
                sent0=sent0.replace('.','')
                sent0=sent0.replace('?','')
                sent0=sent0.replace('!','')
                #if sent0.find('brexit')>-1: # & sent0.find('vaal')>-1
                if all(wrd in sent0 for wrd in searchwords):
                    if sent0!='' and len(sent0)>2:
                        #words=sent0.split(' ')
                        words=re.findall(r"[\w']+", sent0)
                        stemmed=[]
                        for k in words:
                            #t01=stemmer.stem(k)
                            t01=k
                            stemmed.append(t01)

                        date=year+month
                        sentences.append([date,year,month,origsent,len(stemmed),sent0, words,stemmed])
    
    return sentences
