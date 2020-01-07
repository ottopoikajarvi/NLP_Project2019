import matplotlib.pyplot as plt 
import json

with open("time_results.txt", encoding="utf-8") as f:
        file_contents = f.read()
        timedata = file_contents.split("\n")[1]
        json_acceptable_string = timedata.replace("'", "\"")
        timedata = json.loads(json_acceptable_string)

#Edit this to edit the searched word on top of the graph
searched_word = "esimerkki"


plt.figure(figsize=(20,10))
data = []
left = ['2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
for year in left:
        if year in timedata:
                data.append(timedata[year])  
        else:
                data.append(0)
        
tick_label = ['2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']       
plt.bar(left, data, tick_label = tick_label, 
        width = 0.8, color = ['blue', 'grey']) 

plt.xlabel("Year")
plt.ylabel("Amount of word appearances")
plt.title("Word: " + searched_word)
#plt.show()


plt.savefig('figure.png')

