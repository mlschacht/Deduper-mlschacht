#!/usr/bin/env python

import argparse
import gzip
import re

def get_args():
    parser = argparse.ArgumentParser(description="This will remove PCR duplicates from a sorted sam file. As a reminder, this will only keep the first instance of the duplicate and remove all others.")
    parser.add_argument("-f", "--file", help="absolute input file path to sorted sam file", type = str, required = True)
    parser.add_argument("-o", "--outfile", help="for the output path to the new dediplicated sam file", type = str, required = True)
    parser.add_argument("-u", "--umi", help="absolute input file path to umi file", type = str, required = True)
    return parser.parse_args()

args = get_args()
in_sam: str = args.file
out_file: str = args.outfile
umi_file: str = args.umi

#code must be able to run as ./schacht_deduper.py -u STL96.txt -f <in.sam> -o <out.sam>

#comment out test files when ready
# umi_file:str = "STL96.txt" 
# in_sam:str = "test.sam"
# out_file = "test_output.sam"

umi_set:set = set() #initializes empty UMI set

#read in the UMI file
with open(umi_file, "r") as u_file:
    #for all lines in the UMI file
    for num, line in enumerate(u_file):
        line:str = line.strip()
        umi_set.add(line) #add the UMIs into a set

#find 5' start position given pos, cigar, and strand
def VPrimeFinder(pos:int, cigar:str, strand:str) ->  int:
    """Find the 5' start position using the 1 based left most starting position, the cigar string, and the strand (+ or -)."""
    pieces:list = re.findall("[0-9]+[A-Z]", cigar) # make a list of all the number with letter combinations down the string
    cigar_start:str = pieces[0] #take the start number-letter combination of the cigar string
    if strand == "+": #positive strand
        softclipping:int = 0 #initialize soft clipping value
        if 'S' in cigar_start: #if the cigar starts with soft clipping
            softclipping:int = int(re.findall("[0-9]+", cigar_start)[0]) #find the soft clipping value
        VPrimePos = pos - softclipping #go backwards from the position based on soft clipping
    else: #negative strand
        add_length:int = 0 #initialize the length to add to the 5' position
        if 'S' in cigar_start: #if the cigar starts with soft clipping, remove it
            del pieces[0]
        for i, item in enumerate(pieces): #go through the rest of the cigar string number-letter combinations
            num_letter:int = int(re.findall("[0-9]+", item)[0]) #grab the number
            if "I" not in item: #if this number is NOT an insert
                add_length += num_letter #add the number to the length that needs to be added to position
        VPrimePos:int = pos + add_length #go forwards in position avoiding the beginning soft clipping and avoiding inserts

    return VPrimePos #return the 5' position

unique_set:set = set()  #initializes empty UMI set
unique_count = 0        #initialize count of unique reads 
wrong_UMI_count = 0     #initialize count of wrong UMIs
duplicate_count = 0     #initialize count of duplicates removed
soft_clipping_max = 50  #set max clipping
current_chrom:str = "0" #initialize a current chromosome holder

with open(in_sam, "r") as sam, open(out_file, 'w') as o_file:
    for num, line in enumerate(sam):
        # line = sam.readline().strip()
        line = line.strip()
        if line.startswith("@"): #print the header lines that start with "@"
            o_file.write(line)
            o_file.write('\n')
        else: #for the lines with reads
            read:list = line.split()
            umi = read[0].split(':')[-1] #column 0 of read has the qname and the last item after the ':' has the UMI
            if umi in umi_set: #if UMI is in the set, keep going, if not, skip this section and move on
                chrom = read[2] #store the chromosome
                if chrom != current_chrom: #This is a new chromosome!
                    unique_set:set = set() #clear the unique set!
                    current_chrom = chrom 
                left_pos:int = int(read[3]) #store the left-most position
                cigar:str = read[5] #get the cigar string
                flag:int = int(read[1])
                if((flag & 16) ==16): #strand check (reverse complemet check)
                    strand:str = "-" #rev_comp = T = minus strand
                else:
                    strand:str = "+" #rev_comp = F = minus strand
                #get the 5' position
                VPrime = VPrimeFinder(left_pos, cigar, strand)
                read_tuple:tuple= (VPrime, chrom, strand, umi)
                
                #have we seen this read before?
                if read_tuple not in unique_set: #No! We found a unique read!
                    #add tuple to set
                    unique_set.add(read_tuple)

                    #write line out to the file
                    o_file.write(line)
                    o_file.write('\n')

                    #increment unique read counter
                    unique_count +=1

                else: #Yes! We found a duplicate!
                    duplicate_count += 1

            else: #wrong umi
                wrong_UMI_count +=1 #increment wrong umi counter

    # print(read_tuple)

print(f'Number of unique reads: {unique_count}')
print(f'Number of duplicate reads: {duplicate_count}')
print(f'Number of unknown UMI: {wrong_UMI_count}')




