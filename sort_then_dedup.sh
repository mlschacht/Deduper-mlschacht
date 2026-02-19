#!/bin/bash

#SBATCH --account=bgmp                      #REQUIRED: which account to use
#SBATCH --partition=bgmp                    #REQUIRED: which partition to use
#SBATCH --cpus-per-task=1                   #optional: number of cpus, default is 1
#SBATCH --job-name=dedupe                   #optional: job name
#SBATCH --output=sbatch_out/dedupe_%j.out              #optional: file to store stdout from job, %j adds the assigned jobID
#SBATCH --error=sbatch_out/dedupe_%j.err               #optional: file to store stderr from job, %j adds the assigned jobID

#conda activate QAA

#sort the sam file
#samtools sort /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam -o ./sorted_C1_SE_uniqAlign.sam

#dedup the sam file
/usr/bin/time -v ./schacht_deduper.py -u STL96.txt -f ./sorted_C1_SE_uniqAlign.sam -o ./deduped_C1_SE_uniqAlign.sam

#Running Test Files
# Test1: different_length_dups.sam -> different_length_dups_output.sam
# /usr/bin/time -v ./schacht_deduper.py -u STL96.txt -f ./test_files/different_length_dups.sam -o ./test_files/different_length_dups_output.sam

# Test1: input.sam -> output.sam
# /usr/bin/time -v ./schacht_deduper.py -u STL96.txt -f ./test_files/input.sam -o ./test_files/output.sam

#Test2: labeled.sam -> labeled_output.sam
# /usr/bin/time -v ./schacht_deduper.py -u STL96.txt -f ./test_files/labeled.sam -o ./test_files/labeled_output.sam

#Test3: test.sam -> test_output.sam
# /usr/bin/time -v ./schacht_deduper.py -u STL96.txt -f ./test_files/test.sam -o ./test_output.sam