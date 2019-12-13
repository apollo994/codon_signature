#Author: Andreas Blaumeiser, Joint Research Centre F7 Unit, Ispra (Italy)
#Date: 2019-10-09
#TODO: move re-scaling from build_table to get_column_distribution function
 
import argparse
from collections import OrderedDict
import fractions
from functools import reduce
import math
import numpy as np
import operator
import pandas as pd


#parse_table
#Reads in the data from the input file.
#
#Parameters:
#inpath: path to the input file
#
#Output:
#data from the input file transformed into a Pandas dataframe
def parse_table(inpath):
    data = pd.read_csv(inpath, sep='\t', index_col=False, low_memory=False)
    return data


#get_column_distribution
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
def get_column_distribution(data, limit):
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
        total = reduce(lambda x,y: x+y, freqs.values())
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


#build_table
#Creates a table of values for each pair of codons column picked randomly
#with a distribution according to all values in the column.
#
#Parameters:
#distributions: dictionary with the precalculated distributions for the columns
#nr: number of rows that the table should have
#
#Output:
#Pandas dataframe with the random values for each column
def build_table(distributions, nr):
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
        '-i', '--input', metavar='INPUTFILE', default="/dev/stdin",
        help='The input file.'
    )
    parser.add_argument(
        '-o', '--output', metavar='OUTPUTFILE', default="/dev/stdout",
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

    #parse input
    table = parse_table(inpath)
    #build the distributions for the columns
    distributions = get_column_distribution(table, threshold)
    #create the table with the random samples for each column
    training_data = build_table(distributions, nr_rows)
    #write the table as .tsv to the output file
    training_data.to_csv(outpath, sep='\t', index=False)

if __name__ == "__main__":
    main()
