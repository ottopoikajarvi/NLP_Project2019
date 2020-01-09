# NLP_Project2019

Otto Poikajärvi, Julius Hekkala, Aleksi Juurikka

Task 2-4 requires Turku neural parser pipeline running in server mode https://turkunlp.org/Turku-neural-parser-pipeline/
Dataset for task 1: Kielipankki Downloads Suomi 24 Dataset https://korp.csc.fi/download/Suomi24/ (click the folder '2001-2015')

Dataset for tasks 2-4: Yle news 2011-2018 dataset https://korp.csc.fi/download/YLE/fi/

## What you need to do to run task 1 implementation

### NOTICE: The task 1 implementation has only been tested on Windows
The dataset used in the implementation (https://korp.csc.fi/download/Suomi24/, click the folder '2001-2015') requires authentication with a university account. The dataset is quite big (32 GB unzipped). 

To run the scripts, you need to have nltk (https://www.nltk.org/), stop-words (https://pypi.org/project/stop-words/) and matplotlib (https://matplotlib.org/) installed.

context_word_searcher.py searchers for context words of the supplied word. The results are saved in the running directory as context_results.txt. Esimerkki.txt contains an example of how you can supply a word for the script. You need to write different forms of the searched word in a text file as in esimerkki.txt. You can change the name of the file that contains the different word forms in the scripts.

appearance_searcher.py searches for instances of a word in the dataset. The searched word is supplied the same way as with context_word_searcher.py. The results are saved into a text file called time_results.txt.

appearance_visualizer.py visualizes the data in time_results.txt. You need to run appearance_searcher.py before you can run appearance_visualizer.py.

You can change the dataset directory name in the scripts if you want to. Remember to check that the "directoryname" variable points to the correct directory. "search_file" represents the file with the searched word's different forms. Edit the "searched_word" variable in appearance_visualizer.py to edit the word shown in the bar graph.

## What you need to do to run task 2-4 implementation

### NOTICE: The task 2-4 implementation has only been tested on Linux
Requirements: nltk, stop-words, matplotlib, pandas, Turku neural parser pipeline, CoNLL-U Parser https://pypi.org/project/conllu/

Python 3 should start with python3 command in terminal.

Start Turku neural parser pipeline according to the installation guide, use server mode.

Use python-scripts found in data_preparation to prepare the dataset. The pickled sentences-file has to be in the same folder as gui.py, pickleopener.py, plotSentenceLength.py and tnparser_wrap.py. The UI uses tkinter. Run gui.py in order to start the UI. Then use the UI to limit the dataset and send wanted sentences to the Turku neural parser pipeline and to draw figures of the results. 

Output examples:
Words in noun phrases for all sentences with "brexit"
![Words in noun phrases](/allnoun.png)


Main verbs of sentences with "brexit", June 2017
![June 2017 main verbs](/201706verb.png)
"Äänestää" (to vote) is present in the later figure, maybe because of the UK General Election.

