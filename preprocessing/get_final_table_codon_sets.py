#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Fri Dec 13 10:00:23 2019

@author: andreas
'''

#Author: Andreas Blaumeiser, Joint Research Centre F7 Unit, Ispra (Italy)
#Date: 2019-10-09
#TODO: move re-scaling from build_table to get_column_distribution function
 
import argparse
from collections import OrderedDict
import fractions
from functools import reduce
import glob
#import math
import numpy as np
import operator
import pandas as pd


def parse_table(inpath):
#Reads in the data from the input file.
#
#Parameters:
#inpath: path to the input file
#
#Output:
#data from the input file transformed into a Pandas dataframe
    
    data = pd.read_csv(
            inpath, sep='\t', index_col=False, low_memory=False
            )
    data = data.round(2)
    data.drop('Taxid', axis=1, inplace=True)
    data.set_index('Assembly', inplace=True)
    #data.round(2, inplace=True)
    #print(data.columns)
    #print(data)
    return data


def get_codon_distribution(data, outpath, species):
    
    codon_df = pd.DataFrame
    
    synonymous_codons = {
        'CYS': ['TGT', 'TGC'],
        'ASP': ['GAT', 'GAC'],
        'SER': ['TCT', 'TCG', 'TCA', 'TCC', 'AGC', 'AGT'],
        'GLN': ['CAA', 'CAG'],
        'MET': ['ATG'],
        'ASN': ['AAC', 'AAT'],
        'PRO': ['CCT', 'CCG', 'CCA', 'CCC'],
        'LYS': ['AAG', 'AAA'],
        'STOP': ['TAG', 'TGA', 'TAA'],
        #'STOP': ['TAA'],
        #'SEC': ['TGA'],
        #'PYL': ['TAG'],
        'THR': ['ACC', 'ACA', 'ACG', 'ACT'],
        'PHE': ['TTT', 'TTC'],
        'ALA': ['GCA', 'GCC', 'GCG', 'GCT'],
        'GLY': ['GGT', 'GGG', 'GGA', 'GGC'],
        'ILE': ['ATC', 'ATA', 'ATT'],
        'LEU': ['TTA', 'TTG', 'CTC', 'CTT', 'CTG', 'CTA'],
        'HIS': ['CAT', 'CAC'],
        'ARG': ['CGA', 'CGC', 'CGG', 'CGT', 'AGG', 'AGA'],
        'TRP': ['TGG'],
        'VAL': ['GTA', 'GTC', 'GTG', 'GTT'],
        'GLU': ['GAG', 'GAA'],
        'TYR': ['TAT', 'TAC']
        }
    
    nr_assemblies = len(data.index)
    limit = np.floor_divide(nr_assemblies, 100) + 1
    #print(nr_assemblies)
    #print(limit)
    
    #outfile = open('{}/{}_output.tsv'.format(outpath, species), 'w')
    #outfile.write('{}\n'.format(species))
    for amino_acid in synonymous_codons:
        codon_values = data[synonymous_codons[amino_acid]]
        #print(amino_acid)
        #print(codon_values)#
        #Count the absolute frequencies of all combinations of codon values
        frequencies = codon_values.groupby(synonymous_codons[amino_acid]).size().reset_index(name='Frequency')
        #Sort the codon sets according to their frequency
        sorted_freqs = frequencies.sort_values(by='Frequency', ascending=False)
        old_total = sum(sorted_freqs['Frequency'])
        #print(len(sorted_freqs.index))
#        if len(sorted_freqs.index) == 16:
#            print(sorted_freqs)
#            sorted_freqs.drop(sorted_freqs[sorted_freqs.Frequency <= limit].index, inplace=True)
#            print(sorted_freqs)
        #Remove entries that occur less frequent than the limit
        #sorted_freqs = sorted_freqs[sorted_freqs.Frequency <= limit]
        sorted_freqs.drop(sorted_freqs[sorted_freqs.Frequency <= limit].index, inplace=True)
        #new_total = sum(sorted_freqs['Frequency'].values)
        print(sorted_freqs['Frequency'].values)
        #print(old_total)
        #print(new_total)
        #total = sum(sorted_freqs['Frequency'])
        #print(len(sorted_freqs.index))
        #Transform the absolute values into relative ones
        #total = sum(sorted_freqs['Frequency'])
        sorted_freqs['Frequency'] = sorted_freqs['Frequency'].divide(old_total)
        new_total = sum(sorted_freqs['Frequency'].values)
        #print(new_total)
        sorted_freqs['Frequency'] = sorted_freqs['Frequency'].divide(new_total)
        print(sorted_freqs)
        print(sum(sorted_freqs['Frequency'].values))
        #codon_df = pd.merge(codon_df, sorted_freqs)
        #print(sorted_freqs.head(1))
        #top_codons = sorted_freqs.head(1)['Frequency'].values[0].round(2)
        #top_codons = sorted_freqs.head(1)
        #print(top_codons)
        #outfile.write('{}\t{}\n'.format(amino_acid, top_codons))
        #outfile.write()
        #outfile.write('{}\n'.format(amino_acid))
        #outfile.write(sorted_freqs.to_csv(sep='\t', index=False))
        #outfile.write('\n')
        #outfile.write(top_codons.to_csv(sep='\t', index=False))
        #outfile.write('{}\n'.format(sorted_freqs.head(1).to_string(index=False)))
    
    #outfile.close()

#    frequencies = data.groupby(['TAT','TAC']).size().reset_index(name='Frequency')
#    sorted_freqs = frequencies.sort_values(by='Frequency', ascending=False)
#    sorted_freqs['Frequency'] = sorted_freqs['Frequency'].divide(sum(sorted_freqs['Frequency']))
#    print(sorted_freqs)
#    
    #print(frequencies.sort_values(by='Frequency', ascending=False, inplace=True))
    #frequencies.divide()
    #print(frequencies)
    
    #print(data.groupby(['ATG','TAC']).size().reset_index(name='Frequency'))
    #print(data.groupby(['ATG','TAC']).size().reset_index(name='Frequency').sort_values(by=['Frequency'], inplace=True))
    #print(type(data.groupby(['ATG','TAC']).size().reset_index(name='Frequency')))
    #print(pd.crosstab(data.ATG, data.TAC))
    
    #print(data[['ATG','CTG']].value_counts())
    
    
    return None




def build_table(distributions, nr):
#Creates a table of values for each pair of codons column picked randomly
#with a distribution according to all values in the column.
#
#Parameters:
#distributions: dictionary with the precalculated distributions for the columns
#nr: number of rows that the table should have
#
#Output:
#Pandas dataframe with the random values for each column
    
    sample_dict = {}
    #re-scaling to 1 (since it is supposed to be a distribution)
    #Should be moved to get_column_distribution function
    for column in distributions:
        keys = list(distributions[column].keys())
        values = list(distributions[column].values())
        percent = reduce(lambda x,y: x+y, values)
        #Fraction method must be used to avoid floating point issues that will
        #cause the re-scaled values to not add up to 1
        norm_values = [
            fractions.Fraction(value/percent).limit_denominator()
            for value in values
        ]

        if reduce(lambda x,y: x+y, norm_values) != 1:
            print('numerical issue with {}'.format(column))
        else:
            sample = np.random.choice(keys, p=list(norm_values), size=nr)
            sample_dict[column] = sample

    sample_df = pd.DataFrame(sample_dict)
    return sample_df


def main():
    #argument parsing
    parser = argparse.ArgumentParser(description='Codon usage sample tool.')
    parser.add_argument(
        '-i', '--input', metavar='INPUTFILE', default='/dev/stdin',
        help='The input file.'
    )
    parser.add_argument(
        '-o', '--output', metavar='OUTPUTFILE', default='/dev/stdout',
        help='The output file.'
    )
    parser.add_argument(
        '-r', '--rows', metavar='int', type=int, const=10000, default=10000,  
        nargs='?', help='Number of rows for model training.'
    )
    parser.add_argument(
        '-t', '--threshold', metavar='float', type=float, const=0.9,
         help='Threshold for value inclusion.',nargs='?', default=0.9
    )
    args = parser.parse_args()
    
    #defining global parameters according to the command line arguments
    threshold = args.threshold
    nr_rows = args.rows
    inpath = args.input
    outpath = args.output
    
    #taxa = glob.glob('{}/666*.tsv'.format(inpath))
    #taxa = glob.glob('{}/*.tsv'.format(inpath))
    #print(inpath)
    #print(taxa)
    #for taxon in taxa:
    species = inpath.split('/')[-1].split('_')[0]
    table = parse_table(inpath)
        #build the distributions for the columns
        #distributions = get_column_distribution(table, threshold)
    distributions = get_codon_distribution(table, outpath, species)
        
    #filtered_rows = filter_rows(table, distributions)
    #print(distributions.keys())
    #print(distributions)
    #create the table with the random samples for each column
    #training_data = build_table(distributions, nr_rows)
    #write the table as .tsv to the output file
    #training_data.to_csv(outpath, sep='\t', index=False)

if __name__ == '__main__':
    main()




'''
def get_column_distribution(data, limit):
#Finds the most common values for each data column and constructs a
#distribution.
#
#Parameters:
#data: dataframe with all fraction values for the pairs of complementary codons
#limit: the defined threshold of how much percentage of the column should be
#       covered by the selected values
#
#Output:
#dictionary with the most common values per column and the percentage of the
#total column that these values cover    
    
    #the eventual output of the function
    distributions = OrderedDict()
    #find the distribution for each column
    for column_name in data.columns:
        #count the absolute frequencies
        freqs = {}
        column_values = data[column_name].values
        for value in column_values:
            try:
                freqs[value] += 1
            except:
                freqs[value] = 1
        #transform absolute freqs into relative freqs
        #total = reduce(lambda x,y: x+y, freqs.values())
        total = sum(freqs.values())
        freqs = {freq: freqs[freq]/total for freq in freqs}
        #sort the values according to the frequencies to find the maxima
        sorted_freqs = sorted(
            freqs.items(), key=operator.itemgetter(1), reverse=True
        )
        #the highest percentage value
        max_percent = sorted_freqs[0][1]
        #find the list of all maxima
        maxima = [tup[0] for tup in sorted_freqs if tup[1] == max_percent]
        #add the values of the maxima to the column distribution
        for mx in maxima:
            try:
                distributions[column_name][mx] = max_percent
            except:
                distributions[column_name] = {mx: max_percent}
        #check if the maxima already cover more than the threshold because then
        #no need to continue
        percentage = len(maxima)*max_percent
        if percentage >= limit:
            continue
        #if the maxima do not cover the limit, extend the range of values
        else:
            #set to check which values have already been added to avoid
            #repeated considerations of values (all maxima belong to this
            #set by default)
            touched_values = set(maxima)
            #dictionary to keep track of the extension around the maxima
            #0: left neighbor, 1: right neighbor
            maxima_dict = {
                maxi: {0: maxi - 0.01, 1: maxi + 0.01} for maxi in maxima
            }

            #auxiliary function to identify the next best value that should
            #be added to the column's distribution
            def find_next_value(ptg):
                nbr_values = []
                #go through neighbors of all maxima to find new best value
                for maxi in maxima:
                    left = maxima_dict[maxi][0]
                    right = maxima_dict[maxi][1]

                    if not left in touched_values and left in freqs:
                        nbr_values.append(((maxi, 0), freqs[left]))
                    if not right in touched_values and right in freqs:
                        nbr_values.append(((maxi, 1), freqs[right]))

                if nbr_values:
                    next_step = (
                        sorted(nbr_values, key=operator.itemgetter(1),
                               reverse=True)
                    )[0]
                    next_value = maxima_dict[next_step[0][0]][next_step[0][1]]
                    next_max = next_step[1]
                    #update list of touched values
                    touched_values.add(next_value)
                    #update maxima_dict
                    curr_max = next_step[0][0]
                    nbr = next_step[0][1]
                    #values need to be rounded to avoid floating point issues,
                    #e.g. 0.81+0.01=0.8200000000000001 in vanilla Python
                    if nbr == 0:
                        new_left = round(maxima_dict[curr_max][0] - 0.01, 2)
                        maxima_dict[curr_max][0] = new_left
                    elif nbr == 1:
                        new_right = round(maxima_dict[curr_max][1] + 0.01, 2)
                        maxima_dict[curr_max][1] = new_right
                    return (next_value, next_max)
                else:
                    return False

            #if the limit has not been reached yet, more values can be added
            #to the distribution by calling the find_next_value function
            while percentage < limit:
                next_step = find_next_value(percentage)
                if next_step:
                    distributions[column_name][next_step[0]] = next_step[1]
                    percentage = math.fsum([percentage, next_step[1]])
                #limit cannot be reached because the next step reached only
                #zeros (or went out of boundaries - <0 or >1), stop extension
                else:
                    break
                
    return distributions
    
    
    def filter_rows(table, distributions):
    #Find min/max
    min_max_dict = {
        codon: (
                min(distributions[codon].keys()),
                max(distributions[codon].keys())
                )
        for codon in distributions
    }
    #print(min_max_dict)
    
    out_set = set()
    out_dict = {}
    
    for column in table.columns:
        min_value = min_max_dict[column][0]
        max_value = min_max_dict[column][1]
        #print(column, min_max_dict[column])
        for row in table.index:
            #print(column, row)
            #print(table[column][row])
            if table[column][row] >= min_value and table[column][row] <= max_value:
                pass
                #print('IN')
            else:
                print('OUT')
                print(column, row)
                print(table[column][row])
                print(min_max_dict[column])
                out_set.add(row)
                try:
                    out_dict[row] += 1
                except:
                    out_dict[row] = 1
    
    #print(out_set)
    print(len(out_set))
    reduced_table = table.drop(index=list(out_set))
    print(reduced_table)
    #print(out_dict)
    return reduced_table
    #print(min_max_dict)
    
    #print(table.columns)
    #print(table.index)
    
    #Filter rows if their values are not in the min/max range
#    for row in table.itertuples():
#        for value in row:
#            print(value)

'''