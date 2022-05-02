### Strain selection process ###

import numpy as np
import pandas as pd

# Set folder path #
folder = "home/user/Documents/GBS_typeIV/REF"

# Import data file #
alldata = pd.read_csv(folder+'FILE.csv', index_col='POS')
