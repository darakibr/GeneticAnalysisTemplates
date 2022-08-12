import os
import pandas as pd
import re
from datetime import date

today = date.today().strftime("%Y%m%d")
project = input("Name of the project, should match project folder (already containing fastq or illumina raw data files)\
                \nexample: 'GBS_IV': ")

if project in os.listdir():
    os.chdir(project)
else:
    path = input(project+" folder not found in this directory, enter full path: ")
    os.chdir(path)

cwd = os.getcwd()
fastqfolder = [item for item in os.listdir() if item=='fastq']
pathtofastq = cwd+'/'+fastqfolder[0]

### Name all necessary inputs ###
referencefolder = input("Path to reference folder (bacterianickname_reference_files)\nexample: 'GBS_reference_files': ") 
bacteria = input("Name of the bacteria species using underscore and not including  '.fa' '.fasta' or '.txt' extensions\
               \nexample: 'Streptococcus_agalactiae': ")
stdb = input("Standard serotype database fasta file including '.fa' or '.fasta' extensions\
             \nexample: 'GBS_serotype.fa': ")

def prepilluminafiles(pathtofastq, exp_name):
	"""Prepare lists to hold files
	Args:
		fastqfolder (str): Required, default to None. Name of the folder containing files to be renamed.
		exp_name (str): Required, defaults to datetime. Name of experiment to be used in followup analysis.
	Returns:
		samplesinput (str), a ' ' separated string containing all the sample names.
	Raises:
		Error if no files fastq.gz files found with correct two read naming structure.
	"""
	samples = []
	other_files = []
	counter = 0
	def renamefile(filename):
		"""Renames files, and returns new file name as a string.
		Args:
			filename (obj): Required, default to None. Name of the file to be renamed.
		Returns:
			filenamestr (str): String with the new name for the file.
		"""
		filenamestr = str(filename)
		filenamestr = re.sub('_S.+?R','_R', file_rn)
		filenamestr = re.sub('_001','',file_rn)
		os.rename(pathtofastq+filename, pathtofastq+filenamestr)
		return filenamestr
	for file in os.listdir(pathtofastq):
		try:
			if file.endswith("R1_001.fastq.gz"):
				file_rn = renamefile(file)
				samples.append(re.sub('_R1.fastq.gz','', file_rn))
			elif file.endswith("R2_001.fastq.gz"):
				file_rn = renamefile(file)
			elif file.endswith("_R1.fastq.gz"):
				file_rn=str(file)
				samples.append(re.sub('_R1.fastq.gz','',file_rn))
			else:
				other_files.append(str(file))
		except Exception as e:
			raise e
			print("No files found...")
	samplesinput = ' '.join(map(str, samples))
	try:
		outputname = exp_name
	except:
		outputname = now
	with open(outputname+'.txt', "w") as file:
		file.write(samplesinput)
    return samplesinput
	print("================ FINISHED RENAMING FASTQ TO PROPER INPUT NAMES ================")

### Use function on the fastqfolder ###
samples = prepilluminafiles(pathtofastq)

def modifytemplate(template, folder, referencefolder, bacteria, stdb='NONE', samples):
    template
        info = 
        newinfo = re.sub("NAME_OF_FOLDER",folder,info)
        newinfo = re.sub("NAME_OF_REFERENCE_FILE",referencefolder,newinfo)
        newinfo = re.sub("NAME_OF_SPECIES",bacteria,newinfo)
        newinfo = re.sub("NONE",stdb,newinfo)
        newinfo = re.sub("LIST_OF_SAMPLES",samples,newinfo)
        

modifytemplate('TEMPLATE_bac_fastqPipe.sh', cwd, referencefolder, bacteria, stdb, samples)
