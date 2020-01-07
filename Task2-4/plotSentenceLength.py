import matplotlib.pyplot as plt
import pandas as pd

def plotSentenceLength(sentences):
    # Results?
    sentDF=pd.DataFrame(sentences)
    sentDF.columns=['date','year','month','raw','length','lower','words','stemmed']
    meansDF=sentDF.groupby(['date']).mean()
    meansDF['date']=meansDF.index
    meansDF.index.name='index'
    
    mindate=meansDF['date'].min()

    emptyDF=pd.DataFrame({'date':pd.date_range("{:02d}".format(int(mindate[5:6]))+'-01-'+mindate[0:4],'12-31-2018',freq='M').strftime('%Y%m')})

    meansDF=pd.merge(meansDF,emptyDF,how='outer', on=['date'])

    meansDF.sort_values(by=['date']).plot.bar(x='date',y='length',figsize = (13.5, 9))
    plt.savefig('tnparserimages/sentencelength.png')
    plt.show()