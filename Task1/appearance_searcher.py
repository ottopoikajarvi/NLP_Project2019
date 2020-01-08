import json
import os 
import nltk
import time
import multiprocessing

from nltk.stem.snowball import FinnishStemmer
stemmer = FinnishStemmer(ignore_stopwords=True)

#Name of the directory where datasets are located. Edit if necessary
directoryname = "Suomi24-2015-05-25_JSON"

#Change this to the filename of the searched word
search_file = "esimerkki.txt"

global searched_word


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
            message_time = int(message_time / 1000)
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
                        break
                #if the searched word was in the sentence
                if word_found:
                    megalist.append(message_time)
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


#clean up the final list
def process_times(timelist):
    times = []
    for listing in timelist:
        for time in listing:
            times.append(time)
    return times

def get_years(times):
    year_dict = {}
    for timestamp in times:
        year = time.strftime('%Y', time.localtime(timestamp))
        if year in year_dict:
            amount = year_dict[year]
            amount += 1
            year_dict[year] = amount
        else:
            year_dict[year] = 1
    return year_dict

if __name__ == "__main__":
   
    time1 = time.time()
    nltk.download('punkt')
    
    appearance_times = word_searcher(directoryname)
    times = process_times(appearance_times)
    years = get_years(times)
   
    #Write results to time_results.txt
    with open("time_results.txt", "w", encoding="utf-8") as f:
        
        f.write("Times of word appearance: " + str(times))
        f.write("\n")
        f.write(str(years))
        f.write("\n")
        f.write("Word: " + str(searched_word))
        f.close()

    time2 = time.time() - time1
    print("This took " + str(time2) + " seconds")
