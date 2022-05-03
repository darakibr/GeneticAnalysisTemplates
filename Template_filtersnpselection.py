### Strain selection process ###

import numpy as np
import pandas as pd

# Set folder path #
folder = "home/user/Documents/GBS_typeIV/REF"

# Import data file #
alldata = pd.read_csv(folder+'FILE.csv', index_col='POS')
colnames = alldata.columns
annotations = ['ID','I','GN','CDNA','CDS']
cols = annotations

# Subset the data into samples we have access to, removing CDC or other sources
samplesubset = [name for name in colnames if name.find('BCJB') != -1]
cols.extend(samplesubset)
data = alldata[cols]
high = data[data['GN']=='HIGH']
mid = data[data['GN']=='MODERATE']

# FILTER high dataframe to only maintain selected strains #

# FILTER snps rows to only maintain out of suspected PHAGE element snps #
#access PHASTER.ca to obtain... OR from created file to build trees...

# FILTER mid dataframe to select certain strains #
