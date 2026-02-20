# Deduper

## What it is:
This is a repository with a python script built to perform **Reference Based PCR Duplicate Removal**. 
With a sorted sam file of uniquely mapped reads, this script removes all PCR duplicates and outputs a sam file with only 1 copy of each unique read.

A PCR duplicate is defined in this script as a read that contains the same Unique Molecular Identifier (UMI), strand (either + or -), chromosome, and 5' start position.

## How to Run:
An example of how to run the script:
```schacht_deduper.py -u umi_file.txt -f sorted_sam_file.sam -o deduplicated_sam.sam```

Below are options that are required:
    - ```-f```, ```--file```: designates absolute file path to sorted sam file
    - ```-o```, ```--outfile```: designates absolute file path to deduplicated sam file
    - ```-u```, ```--umi```: designates file containing the list of UMIs
    - ```-h```, ```--help```: prints a help message

## Resources in this Repository
The general algorithm designed for this script is described in the pseudocode.md. The algorithm performs in a way that does not load the entire SAM file into memory to be more memory efficient.

The script that performs the deduplication is called schacht_deduper.py. The shell script with commands to run each of the test files is called "test_dedup.sh".

## Dependencies
- Python 3.12 compatible code
- A sorted sam file is needed for this script. Therefore, samtools is needed to sort each sam file before deduplicating if sorting has not occured. This script does not include sorting the file. This needs to be done beforehand.


