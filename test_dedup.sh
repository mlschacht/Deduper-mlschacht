#!/bin/bash

#SBATCH --account=bgmp                      #REQUIRED: which account to use
#SBATCH --partition=bgmp                    #REQUIRED: which partition to use
#SBATCH --cpus-per-task=1                   #optional: number of cpus, default is 1
#SBATCH --job-name=dedupe                   #optional: job name
#SBATCH --output=sbatch_out/test_dedupe_%j.out              #optional: file to store stdout from job, %j adds the assigned jobID
#SBATCH --error=sbatch_out/test_dedupe_%j.err               #optional: file to store stderr from job, %j adds the assigned jobID


#Running Test Files
# Test1: different_length_dups.sam -> different_length_dups_output.sam
/usr/bin/time -v ./schacht_deduper.py -u ./test_files/test_UMI.txt -f ./test_files/different_length_dups.sam -o ./test_output_files/different_length_dups_output.sam

# Test2: input.sam -> output.sam
/usr/bin/time -v ./schacht_deduper.py -u ./test_files/test_UMI.txt -f ./test_files/input.sam -o ./test_output_files/output.sam

#Test3: labeled.sam -> labeled_output.sam
/usr/bin/time -v ./schacht_deduper.py -u ./test_files/test_UMI.txt -f ./test_files/labeled.sam -o ./test_output_files/labeled_output.sam

#Test4: test.sam -> test_output.sam
/usr/bin/time -v ./schacht_deduper.py -u ./test_files/test_UMI.txt -f ./test_files/test.sam -o ./test_output_files/test_output.sam