### Create a BACTERIAL_reference_files folder
#Example is for Staphoria Aureus

class GBS:
    """A Group B Streptococcus (Strep/GBS) genetic sample information class"""
    bacteria = 'Streptococcus_agalactiae'
    abrv = 'GBS'
    def __init__(self, name):
        self.name = name
        self.files = []

class Staph:
    """A Staphylococcus aureus (Staph/SA) genetic sample information class"""
    bacteria = 'Staphylococcus_aureus'
    abrv = 'SA'
    def __init__(self, name):
        self.name = name
        self.files = []
    def addfile(self, filename):
        self.files.append(filename)
    

# create localDB folder
if not found
    create localDB folder
else
    do nothing

# create BACTERIAL.fa
if not found
    search ncbi
    download from ncbi
else
    do nothing

# create header_mlst.txt file
if not found
    open
else
    do nothing

# create BACTERIAL.txt file for MLST
if not found
    open
else
    do nothing
