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
import numpy

def parse_table(inpath):
    data = pd.read_csv(inpath, sep='\t', index_col=False, low_memory=False)
    return data

def get_column_distribution(data, limit):
    distributions = {}
    freqs = {}
    for column_name in data.columns[2:]:
        column_values = data[column_name].values
        for value in column_values:
            try:
                freqs[value] += 1
            except:
                freqs[value] = 1
        #print(list(abs_freqs.values()))
        total = reduce(lambda x,y: x+y, freqs.values())
        #print(total)
        #Transform absolute freqs into relative freqs
        #print(freqs)
        freqs = {freq: freqs[freq]/total for freq in freqs}
        #print(freqs)
        sorted_freqs = sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)
        #rel_freqs = {values[0]: values[1]/total for values in sorted_abs_freqs}
        #print(rel_freqs)
        #print(sorted_freqs)
        index = 0
        max_value = sorted_freqs[index]
        percentage = max_value[1]
        #print(percentage)
        #print(max_value)
        if percentage >= limit:
            distributions[column_name] = {max_value[0]: max_value[1]}
        else:
            #print(percentage)
            while percentage < limit:
                try:
                    #print('1')
                    distributions[column_name][max_value[0]] = max_value[1]
                    #print('2')
                except:
                    distributions[column_name] = {max_value[0]: max_value[1]}
                index += 1
                max_value = sorted_freqs[index]
                percentage += max_value[1]
                #print(percentage)
            distributions[column_name][max_value[0]] = max_value[1]
            
            #distributions[max_value[0]] = 1.0
        #distributions[column_name] = sorted(abs_freqs)
        freqs.clear()
    return distributions

def build_table(distributions, nr):
    
    for column in distributions:
        keys = list(distributions[column].keys())
        values = list(distributions[column].values())
        percent = reduce(lambda x,y: x+y, values)
        norm_values = [round(value/percent, 2) for value in values]
        print(values)
        print(norm_values)
        sample = numpy.random.choice(keys, p=list(norm_values), size=nr)
        print(column)
        print(keys)
        print(sample)
        #print(distributions[column])
        #print(distributions[column].keys())
        #print(distributions[column].values())
        #Construct a vector of nr values drawn from the distribution of column
        None

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
    threshold = 0.9
    nr_rows = 10
    inpath = '/media/andreas/Data/jrc_codon/data/test_table.tsv'
    table = parse_table(inpath)
    distributions = get_column_distribution(table, threshold)
    #print(distributions)
    training_data = build_table(distributions, nr_rows)
    #print(list(table.columns)[2:])
    #for column in table.columns[2:]:
    #    print(table[column])
    #print(table.columns[2:])
    
    
    
    
    


    #generate 10k lines for AI

if __name__ == "__main__":
    main()