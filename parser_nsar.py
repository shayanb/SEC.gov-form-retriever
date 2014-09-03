#!/usr/bin/env python

import sys
import re
import csv
import os.path
from itertools import izip
import shutil
import pandas as pd



#TODO:
#       Read the input file via sysarg or path crawling --> include everything in pathrun()
#           Change the hardcodename argument
#       FIX: Q 8 - 23
#       Joining all the funds to one csv
#    DONE!    series i ! remove the %i from the name of the column
#




hardcodename = "filename" # hard coded name for each fund in each csv - later on this should be changed to a part of the original csv file


def txt2csv(txtfile, csvfilename):
    '''
    converts the txt files to csv files with [Key,Value] structure
    '''
    colonseperated = re.compile(' *(.+) *: *(.+) *')
    fixedfields = re.compile('(\d{3} +\w{6,7}) +(.*)')
    series = re.compile('<(\w{,}.*)>(\w{,}.*)')
    matchers = [colonseperated, fixedfields, series]
    outfile = csv.writer(open(csvfilename +'.csv', 'w'))
    outfile.writerow(['Key', 'Value'])
    for line in open(txtfile):
        line = line.strip()
        for matcher in matchers:
            match = matcher.match(line)
            if match and list(match.groups())[1] not in ('', ' ') and (list(match.groups())[0] not in ('PAGE')):
                outfile.writerow(list(match.groups()))



def pathrun():
    '''
    starts crawling on the ciks folders, opens the txt files and send them to txt2csv
    then runs seriesExtract to extract the series
    '''
    path = os.getcwd()
    path = (path+"/NSAR")
    ciks = os.listdir(path)
    for cik in ciks:
        if cik.isdigit():
            years = os.listdir(path + "/" + cik)
            for i in years:
                os.chdir(path + "/" + cik + "/" + str(i))
                qtrs = os.listdir(".")
                for j in qtrs:
                    os.chdir(path+"/"+cik+ "/" +str(i)+"/"+j)
                    print os.listdir(".")
                    for nsarfile in os.listdir("."):
                        if nsarfile.endswith(".txt"):
                            print str(nsarfile)
                            txt2csv(nsarfile,cik+'-'+i+'-'+j)
                           ## seriesExtract(cik+'-'+i+'-'+j+'.csv') #UNCOMMENT this when series extract is done



csvfile="/Users/sbeta/Desktop/NSARFILES/0000910472-08-000530.csv"


def haveSeries(csvfile):
    '''
    check if the csvfile has any series (funds) returns the line number of 007 A000000 and the number of series
    '''
    with open(csvfile, 'rb') as f:
        reader = csv.reader(f)
        row2 = 0
        for row in reader:
            if (row[0] == '007 A000000') and (row[1]=='Y'):
                baseline = reader.line_num
                print baseline
                seriesnum = reader.next()
                seriesnum1 = seriesnum[1]
                print seriesnum1
                return baseline,seriesnum1
 #           else:
  #              print "NO Funds"
   #             return 0, 0



def transpose(csvfile):
    '''
    transpose the rows and columns of csv file
    '''
    a = izip(*csv.reader(open(csvfile, "rb")))
    filename = os.path.splitext(os.path.basename(csvfile))[0]
    csv.writer(open(filename + "_T.csv", "wb")).writerows(a)



def mergeCsv(filename1,seriesnum):
    """
    goes through all the fund classes and merges the csvs together on inner join
    """
    result = pd.read_csv(filename1 + "_1.csv")
    str = []
    for i in xrange(2,int(seriesnum)): #GO WITH APPEND!
        
        result = result.append(filename1 + "_" + str(i) + ".csv")
       # eachfile = pd.read_csv(filename1 + "_" + str(i) + ".csv")
        #merged = firstfile.merge(eachfile, left_index=True, right_index=True, how='outer')
        #merged.to_csv("result.csv", index=False, na_rep='NA')
    result.to_csv("result.csv")
        #firstfile = pd.read_csv("result.csv").reindex()

        #firstfile.reindex(index="Key")




def writeInCSV(filename,key,value):
    '''
    Hacky code to make/write into a csvfile
    '''
    outfile = csv.writer(open(filename +'.csv', 'a'))
    outfile.writerow([key, value])



def seriesExtract(csvfile):
    '''
    extract fund/series details
    '''
    with open(csvfile, 'rb') as f:
        row2 = 0
        reader = csv.reader(f)

        if haveSeries(csvfile) != False:
            seriesBaseNNum=haveSeries(csvfile)
            for row in reader:  # this part writes all the lines from line number 1 to right before question 7 repeatedly to the quantity of funds
                if reader.line_num < seriesBaseNNum[0]:
                    writeInCSV(hardcodename + "_1", row[0], row[1])
            for i in xrange(2,int(seriesBaseNNum[1])+1): # hacky code to copy the file to the number of funds
                shutil.copyfile(hardcodename + "_1.csv", hardcodename + "_" + str(i) + ".csv")

            f.seek(0)
            #reader2 = csv.reader(f)
            for row in reader:
                for i in xrange(1,int(seriesBaseNNum[1])):
                    seriesi = re.compile ("(?P<qno>\d{3})(?P<qsec>( \w|  )\d{2})%02d(?P<qlast>\d{2}.{,})" %i) # seperate the question number and fund number

                    matchers = seriesi.search(row[0])
                    if matchers:
                        print matchers.group("qno")+ matchers.group("qsec")+matchers.group("qlast")
                        writeInCSV(hardcodename + "_" + str(i), matchers.group("qno")+ matchers.group("qsec")+matchers.group("qlast"),row[1]) # removes the fund number from the question number





#just run pathrun() ... wait for it... TADA!
#pathrun()
#seriesExtract(csvfile)
#for i in xrange(1,16):
#    transpose(hardcodename + "_" + str(i) + ".csv")
mergeCsv(hardcodename, 16)
#transpose("result.csv")
