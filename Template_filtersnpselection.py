### Strain selection process ###

import numpy as np
import pandas as pd

### Set folder path #
folder = "home/user/Documents/GBS_typeIV/REF"

### Import data file #
alldata = pd.read_csv(folder+'FILE.csv', index_col='POS')
colnames = alldata.columns
annotations = ['ID','I','GN','CDNA','CDS']
cols = annotations

### Subset the data into samples we have access to, removing CDC or other sources
samplesubset = [name for name in colnames if name.find('BCJB') != -1]
cols.extend(samplesubset)
data = alldata[cols]
# Create a dictionary with different impact dataframes
data_imp = {g: d for g,d in data.groupby('GN')}

### FILTER high dataframe to only maintain selected strains #
# def impactfilter(data=pd.DataFrame(), impact=('HIGH','MODERATE','LOW','MODIFIER'))
data_imp['HIGH'] #is the dataframe for estimated high impact snps = tt
temp = data_imp['HIGH'].transpose() # = t
temp['HIGHcount'] = data_imp['HIGH'].count() # t with 'c'
high = temp.transpose() # ttt
high['count'] = temp.count() # ttt with 'count'
dropcols = list()
droprows = list()
# select snp rows that appear in over 85% of isolates for removal from consideration
[droprows.append(temp.columns[n]) for n in range(len(high)) if temp.iloc[-1,n] < high['count'].max()-(len(temp)/15)]
# select isolate columns with over 2% snp count from minimal snp count for removal from consideration
[dropcols.append(high.columns[n]) for n in range(len(temp)) if high.iloc[-1,n] > temp['HIGHcount'].min()+(len(high)/50)]

def imp_df_counts(dfdic, impact=None):
    dfdic[impact]
    temp = dfdic[impact].transpose()
    temp[impact+'count'] = dfdic[impact].count()
    newdf = temp.transpose()
    newdf['count'] = temp.count()
    def filterdf(newdf, dft):
        dropcols = list()
        droprows = list()
        [droprows.append(dft.columns[n]) for n in range(len(newdf)) if dft.iloc[-1,n] < newdf['count'].max()-(len(dft)/15)]
        # select isolate columns with over 2% snp count from minimal snp count for removal from consideration
        [dropcols.append(newdf.columns[n]) for n in range(len(dft)) if newdf.iloc[-1,n] > dft['HIGHcount'].min()+(len(newdf)/50)]
    return newdf
  # FILTER snps rows to only maintain out of suspected PHAGE element snps #
#access PHASTER.ca to obtain... OR from created file to build trees...


# FILTER mid dataframe to select certain strains #
data_imp['MODERATE']
