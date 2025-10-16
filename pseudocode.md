## Part 1

## The Problem: PCR Duplicants
PCR duplicates are duplicate reads of the same strand of DNA that occur during PCR amplification during library prep for sequencing. This can occur due to amplification bias where 1 particular strand of DNA is favored to be amplified more than others, which can lead us to incorrectly make assumptions like this DNA comes from RNA of a gene that is highly expressed when really there was an amplification biased that made it look more highly expressed than it really was. In this case, we are creating a reference based PCR duplication removal tool. Therefore, duplicates will be removed after they are aligned to the genome. This will help us reliably remove PCR duplicates instead of accidentally removing sequences that happen to be sequences that are duplicated across the genome in general. Since the reads will already be aligned to a genome, we will be working with a SAM file to identify PCR duplicates. 

Identifying a PCR duplicate includes identifying reads with the same chromosome, strand, 5' start position, and UMI. The chromosome can be identified at position 3 of the header of a sequence. The strand can be identified from the 16th bit of the bitwise flag found at position 2 of the header. The UMI can be found within the first position of the header. The 5' start position is a little more tricky to identify.

There are several conditions to finding the 5'start position:
1. If there is no soft clipping and this is the + strand:
    5' start position = left most mapping position (found in position 4 of the header)

2. If there is no soft clipping and this is on the - strand:
    5' start position = strand length + left most mapping position

3. If there IS soft clipping and this is on the + strand:
    5' start position = left most mapping position - soft clipping at the start of a cigar string

4. If there IS soft clipping and this is on the - strand
    5' start position = left most mapping position + length + soft clipping at the end of the cigar string

Length is the length of the matched/mismatched + any others that hang in the middle of the cigar string like N for skipped region (indicates splicing) or D which indicates a deletion from the sequence, except for I which are instertions and do not align with the genome. (CIGAR string knows the difference because we are aligning to an annotated genome)

After a duplicate is identified, do not write it out to a new SAM file, move on instead.

## Pseudocode
1. Use samtools sort to sort alignments by leftmost coordinates
    - use the -o to write the sorted output to a file rather than to standard out
    - use the -O to specify to output a sam file
2. write all UMIs to a set
2. Open both your input file and the file you want to output those reads that have been de-duplicated
3. write out all lines that start with @

De duplicate:
Proceed through the SAM file read-by-read

1. check if UMI is in the set of known UMIs
    yes - store it for this read
    no - ignore this read and go to the next read
2. store the chromosome from column 3
3. store the strand from column2, the bitwise flag, bit #16 (either + or -)
4. store the 1 based left most starting position
5. store the cigar string
6. Find the 5' start position using the strand, 1 based left most starting position, and the cigar string (holds both reference length and soft clipping information of the read)

Check the stored data:
If this is the first instance of these, write this out to the file and keep these for referencing the next reads.
If this is not the first instance of these (all match what was previously stored), keep what was previously stored and don't write this out to the file.

## High Level Functions
For each function, be sure to include:
    Description/doc string
    Function headers (name and parameters)
    Test examples for individual functions
    Return statement
```python
def fivePrimeFinder(pos:int, cigar:str, strand:bool) ->  int:
    ```Find the 5' start position using the 1 based left most starting position, the cigar string, and the strand. Strand =True means positive strand and false means negative strand.```
    return fivePrimePos:int

    Test examples:
    Input1: 110, 15M, True
    Output1: 110
    Input2: 110, 15M, False
    Output: 125
    Input3: 110, 10S20M, True
    Output3: 100
    Input4: 110, 10S20M, False
    Output4: 130
    Input5: 110, 10S20M5S, True
    Output5: 100
    Input6: 110, 10S20M5S, False
    Output6: 135
    Input7: 110, 23M1290N25M2D18M, True
    Output7: 110
    Input8: 110, 23M1290N25M2D18M, False
    Output8: 1468
    Input8: 110, 23M1290I25M2D18M, False
    Output8: 178
    Input9: 110, 36M12071N29M1S, True
    Output9:110
    Input10: 110, 36M12071N29M5S, False
    Output10:12,251 

#overall, the pos strand only changes with an S on the start and it shouldnt be possible to start with an I
#overall for the neg strand, add all except if there is an S at the front
#if there is an I do not add that value
#do we treat D and N the same? - unsure

def getUMI(qname:str) ->  str:
    ```Find the UMI (8bp in length) within the qname at position 1 of the sam read.```
    #using regex or grabbing the last 8 characters of this string (this may not need to be a function...)
    return fivePrimePos:str

    Test examples:
    Input1: NS500451:154:HWKTMBGXX:1:11101:22955:1351:ATCGAACC
    Output1: ATCGAACC
'''
