#!/bin/bash

### modify these variables ###
threads="34"
genomesize="2200000"

# cwd is: /home/Documents/JCM_SA
### This is the first step in TRYCYCLER PIPELINE, will output cluster data from ONT long read data ###
mkdir -p Trycycler &&
cd Trycycler &&

for X in BCJB1835 BCJB2983 BCJB3343 BCJB3344 BCJB3586 BCJB4361 ; do #For XXXX insert strain or accession numbers#
		cp ../fastq/"$X"_R1.fastq.gz .
		cp ../fastq/"$X"_R2.fastq.gz .
		cp ../../"$folder"/TypeIV/demultiplex/"$X"_ONT.fastq.gz .
		
		#trim ONT reads to >1k and eliminate worst 5% of reads#
		filtlong --min_length 1000 --keep_percent 95 "$X"_ONT.fastq.gz > "$X"_1k5perc.fastq
		
		#Subsampling reads
		trycycler subsample --reads "$X"_1k5perc.fastq --out_dir "$X"_subsets --min_read_depth 75 --count 20 --threads "$threads"
		#Independent assemblies
		mkdir -p "$X"_assemblies
		
		for i in 01 05 09 13 17; do
			canu -p canu -d canu_temp -fast genomeSize="$genome_size" useGrid=false minThreads="$threads" maxThreads="$threads" -nanopore-corrected "$X"_subsets/sample_"$i".fastq -assemble
			mv canu_temp/canu.contigs.fasta > "$X"_assemblies/"$X"assembly_"$i".fasta
			rm -rf canu_temp
		done
		for i in 02 06 10 14 18; do
			flye -g "$genomesize" --nano-corr "$X"_subsets/sample_"$i".fastq --threads "$threads" --out-dir temp_flye &&
			cp temp_flye/assembly.fasta "$X"_assemblies/"$X"assembly_"$i".fasta &&
			rm -r temp_flye
		done
		for i in 03 07 11 15 19; do
			miniasm_and_minipolish.sh  "$X"_subsets/sample_"$i".fastq "$threads" > miniasm_temp.gfa
			any2fasta miniasm_temp.gfa > "$X"_assemblies/"$X"assembly_"$i".fasta
			rm miniasm_temp.gfa
		done
		for i in 04 08 12 16 20; do
			raven --threads "$threads" --disable-checkpoints "$X"_subsets/sample_"$i".fastq > "$X"_assemblies/"$X"assembly_"$i".fasta
		done
		
		#cleanup#
		rm "$X"_ONT.fastq.gz
		rm -r "$X"_subsets
		
		#Tricycler Culster using Mash distance
		trycycler cluster --assemblies "$X"_assemblies/*.fasta --reads "$X"_1k5perc.fastq --out_dir "$X"trycycler_out --threads "$threads"
		### THIS WILL PRODUCE cluster tree graphs, ideally they are very clean
		### If there are 'messy' trees with lots of different lenght branches and strange leafs
		### RENAME 'messy' clustering to start with 'bad_<cluster##>_short' to facilitate continuation of assembly.
		
done
