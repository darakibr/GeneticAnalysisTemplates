### Create a BACTERIAL_reference_files folder
#Example is for Staphoria Aureus
import os
import re
cwd = os.getcwd()

### PICKLE TO SAVE OBJECT
import dill
class bacteria(name, abrv):
    """Creates a class object for bacteria species
    Inputs:
        bacname (str): Name of bacteria species
        bacabrv (str): Common lab abbreviation for bacteria species
    Outputs:
        bacclass (bacteria class object)"""
    def __init__(self, name, abrv):
        self.name = name
        self.abrv = abrv
        self.files = []
        self.isolates = []
    def addfile(self, filename):
        self.files.append(filename)
    def addisolate(self, filename):
        self.isolates.append(filename)

# Attempt to load bacteria class objects
try:
    with open('bacteriaclass.pkl', 'rb') as f:
        SAclass = dill.load(f)
        GBSclass = dill.load(f)
except:
    print('bacteriaclass.pkl not found, no save file containing bacteria class objects in current directory.')

### TO SAVE CLASS OBJECTS
#with open('bacteriaspecies.pkl', 'wb') as file:
 #   dill.dump(SAclass, file)
  #  dill.dump(GBSclass, file)

def add_isolates(classobj, isolatelist):
    """Appends fastq files and name of isolate to the bacteria class object
    Inputs:
        classobj (bacteria class object): object related to bacteria species
        isolatelist (str): list of strings with isolate names, ex. BCJB####
    Outputs:
        None, updates classobj"""
    for isolate in isolatelist:
        classobj.addfile(isolate+'R1.fastq.gz')
        classobj.addfile(isolate+'R2.fastq.gz')
        classobj.addisolate(isolate)

SAclass = bacteria('Staphylococcus_aureus', 'SA')
"""A Staphylococcus aureus (Staph/SA) genetic sample information class"""
GBSclass = bacteria('Streptococcus_agalactiae', 'GBS')
"""A Group B Streptococcus (Strep/GBS) genetic sample information class"""

def searchncbi():
    """Will search the ncbi database for files and/or data.
    """

def createreferencefolder(bacclass):
    bacpath = cwd+'/'+bacclass.abrv+'_reference_file'
    if os.path.exists(bacpath) == True:
        return print('Reference folder for '+bacclass.name+' already exists')
        os.chdir(bacpath)
        bacdir = os.listdir()
        if 'localDB' not in bacdir:
            #create localDB folder
        if bacclass.name+'.fa' not in bacdir:
            #create BACTERIAL.fa
    else:
        os.mkdir(bacpath)
        create localDB folder
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
createreferencefolder(SAclass)
createreferencefolder(GBSclass)
