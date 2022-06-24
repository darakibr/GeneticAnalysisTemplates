### Strain selection process ###

import numpy as np
import pandas as pd

### Set folder path #
folder = "home/user/Documents/GBS_typeIV/REF"
global counter = 0
def savebackup(file):
    global counter +=1
    """Saves a backupfile of the progress in case of Errors or backtracking purposes.
    Args:
      file (obj) : obj to be saved (for this program dataframes to csv files).
    """
    pd.to_csv('temp_'+str(counter)+'.csv')
### Import data file #
alldata = pd.read_csv(folder+'FILE.csv', index_col='POS')
colnames = alldata.columns
annotations = ['ID','I','GN','CDNA','CDS']
### Subset the data into samples we have access to, removing CDC or other sources
samplesubset = [name for name in colnames if name.find('BCJB') != -1]
cols = annotations
cols.extend(samplesubset)
data = alldata[cols]
# Create a dictionary with different impact dataframes
data_imp = {impact: datainfo for impact,datainfo in data.groupby('GN')}

def select_impact(dfdic, impact=('HIGH','MODERATE','LOW','MODIFIER')):
    """Select impact profile from dictionary and add counts to rows and columns.
    Args:
      dfdic (DataFrame Dictionary): dictionary of {impact:dataframes}
      impact (str): label of impact category
    Returns:
      DataFrame: containing only the selected impact category"""
    temp = dfdic[impact]
    temp.loc['snp_count'] = temp.count(numeric_only=True)
    temp['iso_count'] = temp.count(axis=1,numeric_only=True)
    return temp.query('snp_count !=0')

def filterdf(dfdic, impact=('HIGH','MODERATE','LOW','MODIFIER'), perc=0.8, snpsadditional=1):
    """Filters a dataframe to select strains with the fewest number of snps
    Args:
      dfdic (DataFrame Dictionary): dictionary of {impact:dataframes}
      impact (str): String to select impact category to filter.
      perc (float): Float representation of the percentage coverage to be considered representative to the population (default 80%).
      snpsadditional (int): Number of snps in addition to the representative snps to be considered (default 2).
    Returns:
      DataFrame: Selected rows (non 0 or common to at least [default=80]% of strains) and columns (selected strains)."""
    filtered1 = select_impact(df,impact)
    percentmax = int(filtered1['snp_count'].max()*perc)
    filtered2 = filtered1.query('snp_count <= @percentmax')
    
    ------------------ OLD Version#vvv
    dftrans = df.transpose()
    dropcols = list()
    droprows = list()
    [droprows.append(dftrans.columns[n]) for n in range(len(df)) if dftrans.iloc[-1,n] < df['count'].max()-(len(dftrans)*(1-perc))]
    # select isolate columns with over 2% snp count from minimal snp count for removal from consideration
    snpstotal = dftrans['tcount'].replace(0,np.nan).min()+snpsadditional
    [dropcols.append(df.columns[n]) for n in range(len(dftrans)) if df.iloc[-1,n] > dftrans['tcount'].min()+snpstotal)]
    filtered = copy(df)
    filtered.drop(dropcols,axis=1,inplace=True)
    filtered.drop(droprows,axis=0,inplace=True)
    return filtered
    ------------------ OLD Version#^^^

high = filterdf(imp_df_counts(data_imp,'HIGH'), perc=0.8,snpsadditional=2)
moderate = filterdf(imp_df_counts(data_imp,'MODERATE'), perc=0.9,snpsadditional=100)

    #access PHASTER.ca to obtain phage elements... OR 'exclusion .txt file' from files to generate phylo trees...

# FILTER mid dataframe to select certain strains #
data_imp['MODERATE']
