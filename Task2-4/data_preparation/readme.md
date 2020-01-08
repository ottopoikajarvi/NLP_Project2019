# Data preparation
This script fetches and parses the json files in the Yle news archive dataset.

# Getting the dataset
The Yle news archive dataset from years 2011-2018 is available for download at:
https://korp.csc.fi/download/YLE/fi/

# Usage
1. Extract the Yle news dataset the folder called "ylenews-fi-2011-2018-src" as a folder into the same folder as the script
2. Open the python interpreter in the same folder as the script
3. Import the script
4. Use function "searchData(word)" to search for a specific word in the dataset. Give the word you want to search for (as a string) as the function's first argument. The function will then return a list of all the lines that contain the word
5. Pass the results of "searchData(word)" function into parseSentences(hits, searchwords) as it's first argument and give a list of words you want to search for as the second argument. The function then returns the sentences table used in the analysis.

# Example usage

import data_preparation

hits=data_preparation.searchData("brexit")

sentences=data_preparation.parseSentences(hits,["brexit"])