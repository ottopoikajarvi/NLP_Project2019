import json
import os 
import nltk
import time
import multiprocessing
from stop_words import get_stop_words

from nltk.stem.snowball import FinnishStemmer
stemmer = FinnishStemmer(ignore_stopwords=True)

#Edit this if needed
directoryname = "Suomi24-2015-05-25_JSON"

#Change this to the filename of the searched word
search_file = "esimerkki.txt"

global stopwords
global searched_word

#Stopwords
stopwords = get_stop_words('fi')

#The word to be searched
with open(search_file, encoding="utf-8") as f:
        file_contents = f.read()
        searched_word = file_contents.split(",")
        f.close()
#Takes care of going through a single file
def file_processing(file):
    megalist = []
    with open(file, encoding="utf-8") as f: 
        i = 0
        json_file = json.load(f)

        for element in json_file:
            i += 1
            #in case 20 000 elements searched, move on to the next file to speed up the execution
            if i > 20000:
                continue
            message = element['body']
            message_time = element['created_at']
            #clean the messages up
            clean=message.strip().lower()
            clean=clean.replace('\\"','')
            clean=clean.replace('"','')
            clean=clean.replace(',','')
            clean=clean.replace('*','')
            clean=clean.replace('_','')
            clean=clean.replace(':','')
            clean=clean.replace(';','')
            clean=clean.replace('/',' ')
            clean=clean.replace('(','')
            clean=clean.replace(')','')
            clean=clean.replace('-',' ')
            clean=clean.replace('<p>', '')
            clean=clean.replace('< p>', '')
            #tokenize sentences
            sentences=nltk.sent_tokenize(clean, language="finnish")

            
            for sentence in sentences:
                sentence = sentence.strip()
                sentence = sentence.replace('.',' ')
                sentence = sentence.replace('?',' ')
                sentence = sentence.replace('!',' ')
                wordslist = sentence.split(" ")

                #variable to check if the searched word is in the sentence
                word_found = False
                #Check if the searched word is a part of the sentence
                for word in wordslist:
                    if word in searched_word:
                        word_found = True
                        index = wordslist.index(word)
                #if the searched word was in the sentence
                if word_found:
                    #Save the context words (2 to the left and 2 to the right) if they are not stopwords
                    if len(wordslist) > index + 1:
                        neighborword = wordslist[index + 1]
                        if neighborword not in stopwords:
                            megalist.append((neighborword, message_time))
                    if len(wordslist) > index + 2:
                        neighborword = wordslist[index + 2]
                        if neighborword not in stopwords:
                            megalist.append((neighborword, message_time))
                    if index > 0:
                        neighborword = wordslist[index - 1]
                        if neighborword not in stopwords:
                            megalist.append((neighborword, message_time))
                    if index > 1:
                        neighborword = wordslist[index - 2]
                        if neighborword not in stopwords:
                            megalist.append((neighborword, message_time))
        f.close()
    
    return megalist

#Initiate the process
def word_searcher(directory):
    fileList = []
    #Create pool for multiprocessing
    p = multiprocessing.Pool(int(multiprocessing.cpu_count() / 2))
    with os.scandir(directory) as dir:
        #For each file
        for file in dir:
            if file.name.endswith(".json") and file.is_file():
                fileList.append(directory + "/" + file.name)
            
    
    return p.map(file_processing, fileList)

#Go through all the context words and return a dictionary containing the most frequent ones                           
def handle_neighbors(neighbors):
    this_dict = {}
    for listing in neighbors:
        for pair in listing:
            word = stemmer.stem(pair[0])                          
            if word in this_dict and word != '':
                amount = this_dict[word]
                amount += 1
                this_dict[word] = amount
            else:
                this_dict[word] = 1
    #Remove insignificant context words
    pairs_to_pop = []
    for pair in this_dict:
        if this_dict[pair] < 5:
            pairs_to_pop.append(pair)
    for pair in pairs_to_pop:
        if pair in this_dict:
            this_dict.pop(pair)
    return this_dict

#Go through all the times that the word appeared and return them as a list
def handle_times(neighbors):
    times = []
    for listing in neighbors:
        for pair in listing:
            time = int(pair[1] / 1000)
            if time not in times:
                times.append(time)
    return times

if __name__ == "__main__":
   
    time1 = time.time()
    nltk.download('punkt')
    
    list_of_neighbor_words = word_searcher(directoryname)
    common_neighbor_words = handle_neighbors(list_of_neighbor_words)
    appearance_times = handle_times(list_of_neighbor_words)

    #Write results into context_results.txt
    with open("context_results.txt", "w", encoding="utf-8") as f:
        f.write("Word: " + str(searched_word))
        f.write("\n")
        f.write("List of context words: " + str(list_of_neighbor_words))
        f.write("\n")
        f.write("Most common context words: " + str(common_neighbor_words))
        f.write("\n")
        f.write("Searched word appeared this many times with at least one context word: " + str(appearance_times))
        f.close()
    time2 = time.time() - time1
    print("This took " + str(time2) + " seconds")