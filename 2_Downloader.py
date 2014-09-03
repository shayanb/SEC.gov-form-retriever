import os
import re
import os.path

filetype = "NSAR" #put the file/form type here


def ftpfileparser(path,line,year,qtr):
    '''
    Get the links makes the appropriate folders for each CIK and download the file with system's wget
    '''
    splitter = re.compile(r'\t')
    d = dict()
    cleanString = line.strip()
    tokenize = cleanString.split()
    for c in tokenize:
        if c.isdigit() and len(c) > 2:
            temp = c
        if c.startswith("ftp://"):
            d[temp] = c

    for k,v in d.items():

        path = path + "/" + "NSARFILES" # This NSARFILES is hardcoded, change it
        os.chdir(path)
        makedir(k)
        os.chdir(path + "/" + k)
        makedir(year)
        os.chdir(path + "/" + k + "/" + year)
        makedir(qtr)
        os.chdir(path + "/" + k + "/" + year + "/" + qtr)
        os.system("wget " + v)
        print k , " - " , year , " " , qtr , " --- DONE"
#	f.close()



def dlftp():
    '''
    Read the -ftpfiles.txt and send the links to ftpfileparser() to download the files
    '''
    path = os.getcwd()
    for i in xrange(1993,2014):
        os.chdir(path)
        os.chdir(path + "/" + str(i))
        for j in ("QTR1","QTR2","QTR3","QTR4"):
            os.chdir(path + "/" + str(i) + "/" + j)
            f = open('./' + filetype + '-ftpfiles.txt', 'r')
            lines = f.readlines()
            for line in lines:
                ftpfileparser(path,line,str(i),str(j))
                print line, " ", i , " " , j


def makedir(Name):
    dirname = Name
    try:
        os.makedirs(dirname)
    except OSError:
        if os.path.exists(dirname):
            pass
        else:
            raise






dlftp()