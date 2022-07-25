#!/bin/bash

### modify these variables ###
folder="ONT" #  >>> enter the name you want to give folder, will also dictate output names <<< #
REFERENCE="REFISOLATE" # >>> enter the reference isolate name (should match .fa file name) <<< #
threads="34"

# cwd is: /home/Documents/JCM_SA
### This will create the vcf files to be used to call SNP ###
mkdir {hybrid} &&
cd hybrid &&

for X in BCJB1835  ; do #For XXXX insert strain or accession numbers#
		cp ../fastq/"$X"_R1.fastq.gz .
		cp ../fastq/"$X"_R2.fastq.gz .
		cp ../../GBS_ONT/TypeIV/demultiplex/"$X"_ONT.fastq.gz
		
		#trim ONT reads to >1k and eliminate worst 5% of reads#
		filtlong --min_length 5000 --keep_percent 95 "$X"_ONT.fastq.gz > $"X"_5k5perc.fastq
		
		#check read quality using raspberry
		raspberry "$X"_5k5perc.fastq > "$X"_readqc.txt
		#quick cleanup
		rm *.rlen
		
		#Subsampling reads
		trycycler subsample --reads "$X"_5k5perc.fastq --out_dir "$X"_subsets --min_read_depth 300 --threads "$threads"
		#Independent assemblies
		threads="$threads"
		mkdir "$X"_assemblies
		
		flye --nano-hq "$X"_subsets/sample_01.fastq --threads "$threads" --out-dir assembly_01 && cp assembly_01/assembly.fasta "$X"_assemblies/assembly_01.fasta && rm -r assembly_01
		miniasm_and_minipolish.sh "$X"_subsets/sample_02.fastq "$threads" > assembly_02.gfa && any2fasta assembly_02.gfa > "$X"_assemblies/assembly_02.fasta && rm assembly_02.gfa
		raven --threads "$threads" "$X"_subsets/sample_03.fastq > "$X"_assemblies/assembly_03.fasta && rm raven.cereal
		
		flye --nano-hq "$X"_subsets/sample_04.fastq --threads "$threads" --out-dir assembly_04 && cp assembly_04/assembly.fasta "$X"_assemblies/assembly_04.fasta && rm -r assembly_04
		miniasm_and_minipolish.sh "$X"_subsets/sample_05.fastq "$threads" > assembly_05.gfa && any2fasta assembly_05.gfa > "$X"_assemblies/assembly_05.fasta && rm assembly_05.gfa
		raven --threads "$threads" "$X"_subsets/sample_06.fastq > "$X"_assemblies/assembly_06.fasta && rm raven.cereal
		
		flye --nano-hq "$X"_subsets/sample_07.fastq --threads "$threads" --out-dir assembly_07 && cp assembly_07/assembly.fasta "$X"_assemblies/assembly_07.fasta && rm -r assembly_07
		miniasm_and_minipolish.sh "$X"_subsets/sample_08.fastq "$threads" > assembly_08.gfa && any2fasta assembly_08.gfa > "$X"_assemblies/assembly_08.fasta && rm assembly_08.gfa
		raven --threads "$threads" "$X"_subsets/sample_09.fastq > "$X"_assemblies/assembly_09.fasta && rm raven.cereal
		
		flye --nano-raw "$X"_subsets/sample_10.fastq --threads "$threads" --out-dir assembly_10 && cp assembly_10/assembly.fasta "$X"_assemblies/assembly_10.fasta && rm -r assembly_10
		miniasm_and_minipolish.sh "$X"_subsets/sample_11.fastq "$threads" > assembly_11.gfa && any2fasta assembly_11.gfa > "$X"_assemblies/assembly_11.fasta && rm assembly_11.gfa
		raven --threads "$threads" "$X"_subsets/sample_12.fastq > "$X"_assemblies/assembly_12.fasta && rm raven.cereal
		#quick cleanup
		rm -r "$X"_subsets
		#Tricycler Culster using Mash distance
		trycycler cluster --assemblies "$X"_assemblies/*.fasta --reads "$X"_5k5perc.fastq --out_dir trycycler --threads "$threads"
		### THIS WILL PRODUCE cluster tree graphs, ideally they are very clean
		### If there are 'messy' trees with lots of different lenght branches and strange leafs
		### RENAME 'messy' clustering to start with 'bad_<cluster##>' to facilitate continuation of assembly.
		
		
		
		
		#cleanup#
		mv "$f"_ss.txt ./seeker/
		mv "$f"_contigs-1K.fasta ./denovo/
		mv "$f"_readqc.txt ./stats/
		rm -r "$f"_spades-de-novo
		rm *.fastq
		rm *.fastq.gz
		rm "$f"_contigs2.fasta
		rm "$f"_contigs.fasta
		
done
