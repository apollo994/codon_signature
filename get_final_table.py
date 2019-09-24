#Andreas

import os
import sys
import argparse
from collections import defaultdict
import pandas as pd
import numpy as np
import collections
import operator
from functools import reduce

def parse_table(inpath):
    data = pd.read_csv(inpath, sep='\t', index_col=False, low_memory=False)
    return data

def get_column_distribution(data):
    distributions = {}
    abs_freqs = {}
    for column_name in data.columns[2:]:
        column_values = data[column_name].values
        for value in column_values:
            try:
                abs_freqs[value] += 1
            except:
                abs_freqs[value] = 1
        print(list(abs_freqs.values()))
        total = reduce(lambda x,y: x+y, abs_freqs.values())
        print(total)
        sorted_abs_freqs = sorted(abs_freqs.items(), key=operator.itemgetter(1), reverse=True)
        #print(sorted_abs_freqs)
        max_value = sorted_abs_freqs[0]
        mv_percent = max_value[1]/total
        print(mv_percent)
        #print(max_value)
        distributions[column_name] = sorted(abs_freqs)
        abs_freqs.clear()
    return distributions

def build_table(distributions, nr):
    rows = []
    return rows

def main():

    '''
    parser = argparse.ArgumentParser(description='My nice tool.')
    parser.add_argument('--input', metavar='INPUTFILE', default="/dev/stdin", help='The input file.')
    #parser.add_argument('--id', metavar='ID',help='RefSeq tax ID',type=int)
    parser.add_argument('--output', metavar='OUTPUTFILE', default="/dev/stdout", help='The output file.')
    args = parser.parse_args()
    '''
    
    nr_rows = 10
    inpath = '/media/andreas/Data/jrc_codon/data/test_table.tsv'
    table = parse_table(inpath)
    distributions = get_column_distribution(table)
    #print(distributions)
    training_data = build_table(distributions, nr_rows)
    #print(list(table.columns)[2:])
    #for column in table.columns[2:]:
    #    print(table[column])
    #print(table.columns[2:])
    
    
    
    
    


    #generate 10k lines for AI

if __name__ == "__main__":
    main()
