import re
import os
import zipfile,os.path


formtype = 'NSAR' ## form type goes here, e.g NSAR, ADV


def formparser(nsarfile):
	splitter = re.compile(r'\t')

	f = open(nsarfile, 'r')
	fout = open('./' + formtype +'-ftpfiles.txt', 'w')

	lines = f.readlines()
	d = dict()

	for line in lines:
		cleanString = line.strip()
		tokenize = cleanString.split()
		for c in tokenize:
			if c.isdigit() and len(c) > 2:
				temp = c;	
			if c.startswith("edgar/data"):
				d[temp] = c;

	for k,v in d.items():
	    fout.write(k +'\t' + "ftp://ftp.sec.gov/" + v + '\n') 

	f.close()
	fout.close()


def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)


def nsarextract(file): #extract NSAR files from form.idx, NOW any filetype
	f = open(file, 'r')
	fout = open('./' + formtype + '-ftp.txt', 'w')
	lines = f.readlines()
	for line in lines:
	#	c = line.strip()
		if line.startswith(formtype):
			fout.write(line)
			fout.write("\n") 

	f.close()
	fout.close() 



def makedir(Name):
	dirname = Name
	try:
		os.makedirs(dirname)
	except OSError:
		if os.path.exists(dirname):
			pass
		else:
			raise


def formdl(): # to download all the form files in relative folders
	path = os.getcwd()
	for i in xrange(1993,2014):
		os.chdir(path)
		makedir(str(i))
		os.chdir(path + "/" + str(i))
		for j in ("QTR1","QTR2","QTR3","QTR4"):
			print i,j
			makedir(j)
			os.chdir(path + "/" + str(i) + "/" + str(j))
			os.system("wget " + "ftp://ftp.sec.gov/edgar/full-index/" + str(i) + "/" + str(j) + "/form.zip")
			unzip ("form.zip", "./")
			nsarextract("form.idx")
			formparser(formtype + "-ftp.txt")
			os.chdir(path + "/" + str(i))




formdl()




