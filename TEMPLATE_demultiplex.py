### This will create a Sample Sheet for Illumina Output data ###
### This code is meant to be used in combination with TEMPLATE_LIB_PREP.xlsx

import os
import re
import pandas as pd
import numpy as np
from datetime import date

today = date.today().strftime("%Y%m%d")
cwd = os.getcwd()

# Read in Illumina IDT labels to identify samples with corresponding index
idt = pd.read_csv("illumina_IDT.csv")

#Template header required
header = "[Header],,,,,,,,,\
\nInvestigator Name,INVNAME,,,,,,,,\
\nExperiment Name,EXPERIMENT,,,,,,,,\
\nDate,TODAYDATE,,,,,,,,\
\nWorkflow,GenerateFASTQ,,,,,,,,\nApplication,FASTQ Only,,,,,,,,\
\nInstrument Type,INSTRUMENT,,,,,,,,\
\nAssay,Nextera DNA Flex,,,,,,,,\nIndex Adapters,IDT-ILMN Nextera DNA UD Indexes (384 Indexes),,,,,,,,\
\nDescription,DESC,,,,,,,,\
\nChemistry,Amplicon,,,,,,,,\n,,,,,,,,,\
\n[Reads],,,,,,,,,\nREADCYCLES,,,,,,,,,\nREADCYCLES,,,,,,,,,\
\n,,,,,,,,,\n[Settings],,,,,,,,,\nReverseComplement,0,,,,,,,,\n,,,,,,,,,\n[Data],,,,,,,,,"

def createSampleSheet(data):
    investigator_name = input("Investigator Name:\n")
    project = input("Name of project (avoid using spaces):\nEx. StaphoriaRun\n")
    today_date= date.today().strftime("%-d/%-m/%y")
    description = input("Description of run:\nEx. Staph_GBSmut_date\n")  
    runtype = input("Type N for a NextSeq run or M for a MiSeq run:\n")
    if runtype == "N":
        instrument_type = "NextSeq"
        read_cycles = 151
    elif == "M":
        instrument_type = "MiSeq"
        read_cycles = 301
    else:
        runtype = input("Invalid input, please use either 'N' for NextSeq or 'M' for MiSeq only.\n")

    with open('SampleSheet_'+project+today+'.csv', 'w') as file:
        tempheader = header
        tempheader = re.sub('INVNAME',investigator_name, tempheader)
        tempheader = re.sub('EXPERIMENT',project, tempheader)
        tempheader = re.sub('TODAYDATE',today_date, tempheader)
        tempheader = re.sub('INSTRUMENT',instrument_type, tempheader)
        tempheader = re.sub('DESC',description, tempheader)
        tempheader = re.sub('READCYCLES',read_cycles, tempheader)
        file.write(tempheader)
        file.write(data)
    return print("Finished creating SampleSheet file as 'SampleSheet_"+project+today+".csv located in "+cwd)

def createcsvfile(idt):
    libprep_path = input("Path to the library prep excel:")
    input_data = pd.read_excel(libprep_path, sheet_name = "SampleSheet")
    final = pd.DataFrame(columns = \
        ['Sample_ID','Sample_Name','Sample_Plate','Sample_Well','I7_Index_ID','index,I5_Index_ID','index2','Sample_Project','Description']
    final['Sample_ID'] = input_data['Shorthand']
    final['Sample_Name'] = input_data['Sample_Name']
    final['Sample_Plate'] = input_data['Index_Plate']
    final['Sample_Well'] = input_data['Index_Plate_Well']
    final['I7_Index_ID'] = input_data['I7_Index_ID']
    final['index'] = input_data['index']
    final['I5_Index_ID'] = input_data['I5_Index_ID']
    final['index2'] = input_data['index2']
    final['Sample_Project'] = input_data['Sample_Project']
    final['Description'] = ""
    final.replace("#N/A",np.nan,inplace=True)
    final.dropna(axis=0, how='any', subset=['I7_Index_ID','index,I5_Index_ID','index2'], inplace=True)
    final.to_csv(today+'csvdata.csv', index=False)
    return print("Generated data for the SampleSheet and saved as "+today+"csvdata.csv located in "+cwd)

createcsvfile(idt)
with open(today+'csvdata.csv', 'r') as csvfile:
    csvdata = csvfile.read()
    createSampleSheet(csvdata)
