#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:10:30 2019

@author: blauman
"""

import argparse
from Bio import SeqIO
import fractions
import os
import sys


def count_codons_frequencies(inpath):

    codons_dict = { 
        "TTT": 0, "TTC": 0, "TTA": 0, "TTG": 0, "CTT": 0, "CTC": 0, "CTA": 0,
        "CTG": 0, "ATT": 0, "ATC": 0, "ATA": 0, "ATG": 0, "GTT": 0, "GTC": 0,
        "GTA": 0, "GTG": 0, "TAT": 0, "TAC": 0, "TAA": 0, "TAG": 0, "CAT": 0,
        "CAC": 0, "CAA": 0, "CAG": 0, "AAT": 0, "AAC": 0, "AAA": 0, "AAG": 0,
        "GAT": 0, "GAC": 0, "GAA": 0, "GAG": 0, "TCT": 0, "TCC": 0, "TCA": 0, 
        "TCG": 0, "CCT": 0, "CCC": 0, "CCA": 0, "CCG": 0, "ACT": 0, "ACC": 0,
        "ACA": 0, "ACG": 0, "GCT": 0, "GCC": 0, "GCA": 0, "GCG": 0, "TGT": 0,
        "TGC": 0, "TGA": 0, "TGG": 0, "CGT": 0, "CGC": 0, "CGA": 0, "CGG": 0,
        "AGT": 0, "AGC": 0, "AGA": 0, "AGG": 0, "GGT": 0, "GGC": 0, "GGA": 0,
        "GGG": 0
    }

    with open(inpath) as infile:
        seq_records = SeqIO.to_dict(SeqIO.parse(infile, 'fasta'))
        for seq_record in seq_records:
            sequence = seq_records[seq_record].seq.upper()
            if not len(sequence)%3 == 0:
                print('The sequence length is not a multiple of 3.')
                continue
            else:    
                codons = [sequence[i:i+3] for i in range(0, len(sequence), 3)]
                
                for triplet in codons:
                    codons_dict[triplet] += 1

        #Transform absolute frequencies into relative ones.
        total = sum(codons_dict.values())
        
        for codon in codons_dict:
            value = codons_dict[codon]
            codons_dict[codon] = (
                    value,
                    fractions.Fraction(value/total).limit_denominator()
            )

        return codons_dict
    

def main():
    #Input FASTA file    
    parser = argparse.ArgumentParser(description='Codon usage sample tool.')
    parser.add_argument(
        '-i', '--input', metavar='INPUTFILE', default="/dev/stdin",
        help='The input file.'
    )
    args = parser.parse_args()
    inpath = args.input
    
    if not os.path.isfile(inpath):
        sys.exit('Inpute file does not exist.')
    else:
        frequencies = count_codons_frequencies(inpath)       
        print(frequencies)
            
if __name__ == "__main__":
    main()