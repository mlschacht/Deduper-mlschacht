# README - Test Files and How to Use Them

In the test_files directory, there are 4 different test files with their expected outputs that can be used to test different test cases. Below is a list of each test file and the cases they cover.

All test files are intended to be tested with the UMI text file in the main repo directory called "STL96.txt".

## different_length_dups.sam -> different_length_dups_output.sam
- includes 2 reads, which are duplicates but have different UMIs
- should remove
    - the 2nd read
### Stats Output:
Number of unique reads: 1
Number of duplicate reads: 1
Number of unknown UMI: 0


## labeled.sam -> labeled_output.sam
- easiest test file to test
- each read is labeled as either 
    -**"R"** for a read that the deduper script should keep in the output OR
    -**"D"** as a duplicate read that should be removed
- these labels can be found in the 2nd field after the cigar string
- the output should only contain reads labeled R1-R6
### labeled.sam Test Cases:
R1+D1 - have the same values for all fields related to UMI, strand, chromosome, 5' start
R2+D2 - have different lengths in the cigar string but are still duplicates 
R3 - is unique in UMI from R2
R4 + R5 - have different strands
R6 - has a unique UMI and start
### Stats Output
Number of unique reads: 6
Number of duplicate reads: 2
Number of unknown UMI: 0


## input.sam -> output.sam
- should remove 
    - the 2nd read that starts at 700 even though the cigar string is different ("55M")
    - the 4th read that starts at 750 with the same UMI as read 3 ("ACTGTCAG")
- should keep 
    - first read
    - the 3rd and 5th reads as they differ by UMI
    - both 900 reads as they have different directionality
    - the last read
### Stats Output:
Number of unique reads: 6
Number of duplicate reads: 2
Number of unknown UMI: 0

## test.sam -> test_output.sam
- takes the first 100 lines of an actual sam file for fast testing
### Stats Output
Number of unique reads: 54
Number of duplicate reads: 21
Number of unknown UMI: 1