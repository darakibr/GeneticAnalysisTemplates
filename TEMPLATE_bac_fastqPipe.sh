#!/bin/bash

##### PIPELINE USED FOR ANALYSIS OF ILLUMINA GENETIC SEQUENCING DATA #####

	### FOR SRST2, dependent on older versions of bowtie ###
# set PATH to include srst2 if it exists #
if [ -d "$HOME/gen-soft/srst2" ] ; then
	PATH="$HOME/gen-soft/srst2/scripts:$PATH"
fi
# set PATH to include bowtie2 for srst2 if it exists #
if [ -d "$HOME/gen-soft/bowtie2-2.2.9" ] ; then
	PATH="$HOME/gen-soft/bowtie2-2.2.9/bowtie2-2.2.9:$PATH"
fi
# set PATH to include samtools (old version) for srst2 if it exist #
if [ -d "$HOME/gen-soft/samtools" ] ; then
	PATH="$HOME/gen-soft/samtools:$PATH"
fi

### Name all necessary inputs ###
folder="$HOME/Documents/NAME_OF_FOLDER"
# example: "$HOME/Documents/GBS_IV"
referencefolder="NAME_OF_REFERENCE_FILE"
# example: "SA_reference_files" this must match the folder name including necessary files/databases for mlst and/or serotyping.
bacteria="NAME_OF_SPECIES"
# example: "Streptococcus_agalactiae" DO NOT include '.fa' '.fasta' or '.txt' extensions.
stdb="NONE"
# example: "GBS_serotype.fa" *INCLUDE ',fa' or '.fasta' extension. IF NOT needed leave as "NONE"
samples="LIST_OF_SAMPLES" # Copy and paste a ' ' separated list of sample names
# example: "sample1 sample2 sample3" must match .fastq file names excluding '_R1.fastq.gz' ending.

### CREATE all necessary output folders ###
cd "$folder"
mkdir -p corr seeker denovo readqc SPAdeslog MLST/out serotype/out AMR/amrtxt AMR/amrjson metaoutput &&

### START OF ANALYSIS ###
# insert string containing all samples separated by a ' ' where 'LIST_OF_SAMPLES' is located #sample1 sample2 sample3 ...
for X in "$samples" ; do
		cp ./fastq/"$X"_R1.fastq.gz . &&
		cp ./fastq/"$X"_R2.fastq.gz . &&
		
		#trim R1 reads to 25k (100k lines) for strainseeker#
		gzip -d "$X"_R1.fastq.gz &&
		head -n 100000 "$X"_R1.fastq >"$X"_R1-25k.fastq &&
		gzip "$X"_R1.fastq &&
		
		#strainseeker#
		perl ~/gen-soft/strainseeker/seeker.pl -i "$X"_R1-25k.fastq -d ~/gen-soft/strainseeker/ss_db_w32_4324 -o "$X"_ss.txt &&
		echo "	*** done with Strainseeker for $X"
		### START SPADES de novo assembly; saves corrected reads for use in subsequent steps ###
		spades.py -t 28 -1 "$X"_R1.fastq.gz -2 "$X"_R2.fastq.gz -o "$X"_spades-de-novo  &&
			#cleanup
		cd "$X"_spades-de-novo/corrected/ &&
		mv "$X"_R1.fastq.00.0_0.cor.fastq.gz ../../corr/"$X"_R1-corr.fastq.gz &&
		mv "$X"_R2.fastq.00.0_0.cor.fastq.gz ../../corr/"$X"_R2-corr.fastq.gz &&
		cd .. &&
		mv contigs.fasta ../"$X"_contigs.fasta &&
		mv spades.log ../SPAdeslog/"$X"_spades.log &&
		cd .. &&
		echo "	*** done with SPAdes for $X"
		### RENAME contigs ###
		awk '/^>/{print ">""'"$X"'""_contigs-" ++i; next}{print}' < "$X"_contigs.fasta > "$X"_contigs2.fasta &&
		
		### Remove contigs <4, removesmalls.pl program path not set in profile yet ###
		perl ~/gen-soft/removesmalls.pl 1000 "$X"_contigs2.fasta >"$X"_contigs-1K.fasta &&
		
		#Raspberry for qc on corrected reads#
		raspberry ./corr/"$X"* >"$X"_readqc.txt &&
		rm ./corr/*.rlen
		echo "	*** done with read_quality for $X"
			#cleanup
		mv "$X"_ss.txt ./seeker/ &&
		mv "$X"_contigs-1K.fasta ./denovo/ &&
		gzip ./denovo/"$X"_contigs-1K.fasta
		mv "$X"_readqc.txt ./readqc/ &&
		rm -r "$X"_spades-de-novo &&
		rm *.fastq &&
		rm *.fastq.gz &&
		rm "$X"_contigs2.fasta &&
		rm "$X"_contigs.fasta &&
		
		echo "	*** Starting analysis on gene seq"
		cd ~/Documents/"$referencefolder"/ &&
		
		### MLST ###
    # Requires correct MLST input files for bacterial species, refer to necessary input files.
    if [ -e "$bacteria".fasta ]
    then
        if (( -e "$bacteria".txt ))
        then
		        cp "$folder"/fastq/"$X"_R1.fastq.gz ./"$X"_1.fastq.gz &&
	    	    cp "$folder"/fastq/"$X"_R2.fastq.gz ./"$X"_2.fastq.gz &&
	    		    # srst2 command
	    	    srst2.py --threads 20 --output "$X" --input_pe "$X"_*.fastq.gz --mlst_db "$bacteria".fasta --mlst_definitions "$bacteria".txt --mlst_delimiter '_' &&
		        	#cleanup
    	    	mv "$X"__mlst__"$bacteria"__results.txt "$folder"/MLST/out/"$X"_mlst.txt &&
        		rm *.pileup &&
	         	rm *.bam &&
	        	echo "	*** Done with MLST for $X"
        else
            echo "***** MLST with srst2.py not run due to incompatible SPECIES.txt file. *****"
        fi
    else
        echo "***** MLST with srst2.py not run due to incompatible SPECIES.fasta or SPECIES.fasta file. *****"
    fi
		
		### SEROTYPE ###
    if [ -e "$stdb" ]
    then
		    srst2.py --input_pe "$X"_1.fastq.gz "$X"_2.fastq.gz --gene_db "$stdb" --gene_max_mismatch 10 --min_coverage 98 --min_depth 10 --max_divergence 1 --output "$X" --threads 20 &&
		    #mismatch changed from 1 to 10, depth from 15 to 10, divergence from 0 to 1#
			    #cleanup
		    mv "$X"__fullgenes__"$stdb"__results.txt "$folder"/serotype/out/"$X"_serotype.txt &&
		    rm "$X"__*.bam &&
		    rm "$X"__*.pileup &&
	    	rm "$X"__genes*.txt &&
    		rm "$X"_1.fastq.gz &&
	    	rm "$X"_2.fastq.gz &&
	    	echo "	*** Done with serotyping for $X"
    else
        echo "***** srst2.py not run due to no serotype database provided *****"
		fi
    
		### AMR calling ###
		cp "$folder"/denovo/"$X"_contigs-1K.fasta.gz . &&
		gunzip "$X"_contigs-1K.fasta.gz &&
		rgi main --input_sequence "$X"_contigs-1K.fasta --output_file "$X" --input_type contig --num_threads 20 --local --clean &&
			#cleanup
		rm "$X"_contigs-1K.fasta &&
		mv "$X".txt "$folder"/AMR/amrtxt/ &&
		mv "$X".json "$folder"/AMR/amrjson/ &&
		echo "	*** done with AMR calling for $X"
    
done

cd "$folder"/MLST/ &&
head -1 ./out/header_mlst.txt > ../metaoutput/all_mlst.txt && tail -n +2 -q ./out/*.txt >> ../metaoutput/all_mlst.txt &&
cd ../serotype
cat ./out/*.txt > ../metaoutput/all_serotype.txt
cd ../AMR/ &&
rgi heatmap -i ./amrjson -clus both -f &&
mv ./*.csv ../metaoutput/ &&
cd ../seeker/ &&
cat *.txt > ../metaoutput/all_seeker.txt &&
echo "Done combining MLST, serotype and AMR data"
