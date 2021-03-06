#!/usr/bin/env python3
import csv
import math
import os
import sys

def custom_reader(filename, full = True):
    """
    read a input txt file
    :param filename: filename to read
    :param full: can read full data or part of data
    :return: valid record(OTHER_ID field is empty)
    """
    index= [0,10,13,14,15]
    records = []
    short_range = 5000
    with open(filename,'r') as input:
        if full:
            print('Running full data')
            for line in input:
                ind = line.strip().split("|")
                if ind[0] and ind[14] and not (ind[15]):  ##Assume skip the record with empty CMTE_ID or empty TRANSACTION_ID or non-empty OTHER_ID
                    ind[10] = ind[10][:5]   ##only consider the first five characters of the ZIP_CODE
                    records.append([ind[i] for c, i in enumerate(index)])
                else:
                    print(ind)
                    print('Invalid record. Moving to next record')

        else:
            print('Testing with short read')
            for i in range(short_range):
                ind = input.readline().strip().split("|")
                if ind[0] and ind[14] and not (ind[15]):
                    ind[10] = ind[10][:5]   #only consider the first five characters of the ZIP_CODE
                    records.append([ind[i] for c, i in enumerate(index)])
                else:
                    print(ind)
                    print('Invalid record. Moving to next record')
    return records

def zipRecordFilter(records):
    """
    :param records:
    :param  filter valid record for ZIP_CODE field
    :return: filtered records
    """
    return (records[1] and len(records[1]) == 5 and records[1].isdigit())


def dateRecordFilter(records):
    """
    :param records:
    :param filter valid record for TRANSACTION_DT field
    :return: filtered records
    """
    return (records[2] and len(records[2]) == 8 and records[2].isdigit())

def medianvalsProcess(records, mode):
    """
    Compute median running median of contributions, total #transaction, total amount
    :param records: the filtered records for processing medianval by zip or by date
    :param mode: 1: for zip; 2: for date
    :return: zip_output or date_output
    """
    dict = {}
    medianvals = []
    if mode == 1:
        filter(zipRecordFilter, records)
    elif mode == 2:
        filter(dateRecordFilter, records)

    for ind in records:
        key = str(ind[0]) + '|'+ str(ind[mode]) #zip
        if key in dict:
            list = dict.get(key)
        else: list = []
        insert_ind = binary_search(list, int(ind[3]))
        list.insert(insert_ind, int(ind[3]))
        dict[key] = list
        if mode == 1:           ##for zip_output, process input zip_record line by line
            medianvals.append(key + '|' + str(get_median(list)) + '|' + str(len(list)) + '|' + str(sum(list)))
    if mode == 2:               ##for zip_output, process input zip_record and summarized by recipient and date
        sorted(dict.keys())
        for key in dict:
            list = dict.get(key)
            medianvals.append(key + '|' + str(get_median(list)) + '|' + str(len(list)) + '|' + str(sum(list)))
    return medianvals



def get_median(sorted_list):
    """
    As the input is a list sorted in ascending order, the median is the element(s) in the middle of the list
    """
    half = len(sorted_list) // 2
    return int(round((sorted_list[half] + sorted_list[~half]) / 2))

def binary_search(sorted_list, target):
    """
    binary search function, return the location in which the new element should be inserted. To maintain a list sorted by TRANSACTION_AMT in asccending order
    """
    if sorted_list == None:
        return 0
    start, end = 0, len(sorted_list) - 1
    while(start < end):
        mid = int((start + end) / 2)
        if(target == sorted_list[mid]):
            return mid
        elif(target < sorted_list[mid]):
            end = mid - 1
        else:
            start = mid + 1
    if target <= start:
        return start
    else:
        return start


def writeOutput(output, outputLoc):
    """
    write output files
    Args: *output(list of Strings)
    """
    print('writing output')
    f = open(outputLoc[0], 'w')
    for line in output[0]:
        f.write(line + '\n')

    f = open(outputLoc[1], 'w')
    for line in output[1]:
        f.writelines(line + '\n')

    print('finished writing output')



def main(*argv):
    ###define default inputs
    try:
        scriptLoc = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    except:
        scriptLoc = os.path.dirname(os.path.abspath(sys.argv[0]))

    input_file = scriptLoc+os.sep+'input'+os.sep + 'itcont.txt'

    ###define default outputs
    outputLoc1 = scriptLoc + os.sep + 'output' + os.sep + 'medianvals_by_zip.txt'
    outputLoc2 = scriptLoc + os.sep + 'output' + os.sep + 'medianvals_by_date.txt'

    records = custom_reader(input_file, True)
    zip_output = medianvalsProcess(records, 1)
    date_output = medianvalsProcess(records, 2)
    writeOutput([zip_output,date_output],[outputLoc1, outputLoc2])
if __name__ == "__main__":
    if len(sys.argv)>1:
        main(sys.argv[1:])
    else:
        main()
