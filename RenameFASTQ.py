### This program will prepare demultiplexed fastq files for analysis
	# Program used to demultiplex is bcl-convert from Illumina data (MiSeq or NextSeq)
### This will rename the fastq files and prepare a sample text file

### load libraries
import os
import re

### Paths saved to variables
cwd = os.getcwd()
fastqfolder = cwd+"/fastq/"

def prepilluminafiles(fastqfolder):
	"""Prepare lists to hold files
	Args:
		fastqfolder (str): Required, default to None. Name of the folder containing files to be renamed. 
	Returns:
		None, but will rename all files in the folder.
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
		os.rename(fastqfolder+filename, fastqfolder+filenamestr)
		return filenamestr
	for file in os.listdir(fastqfolder):
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
	with open("samples.txt", "w") as file:
		file.write(samplesinput)
	print("================ FINISHED RENAMING FASTQ TO PROPER INPUT NAMES ================")

### Use function on the fastqfolder ###
prepilluminafiles(fastqfolder)
