from Bio import SeqIO 
import os.path
import traceback

def mainMenu():
	self = geneFunctions()
	print("Welcome to the GenBank File Tool.7\nPlease select from the following options:")
	for num, s in enumerate(self.options.keys()):
		print("{}\t{}".format(num+1, s))
	choice = raw_input("Choose an option (0 to quit): ")
	while True:
		try:
			choice = int(choice)
			if choice == 0:
				return
		except ValueError as vErr:
			choice=raw_input("Invalid input. Please enter a number, 0 to quit: ")
	
		else:
			func = getattr(geneFunctions, self.options[self.options.keys()[choice-1]])
			if callable(func):
				print func.__doc__
				valid={'y':True, 'ye':True, 'yes':True, 'n':False, 'no':False}
				while True:
					yn = raw_input("Run function Y/N? >")
					yn = yn.lower()
					if yn='': break
					if yn not in valid:
						print("Please response with y or n.")
					elif valid[yn]:
						func()
					else: 
						mainMenu()				
			break

def pickOneFile(foldername):
	fileList = []
	folder = "./{}/".format(foldername)
	for dirpath, subdirs, files in os.walk(folder):
		if dirpath==folder:
			for x in files:
				x=x.split('.')
				ext = x.pop()
				filename='.'.join(x)
				fileList.append([filename, ext, dirpath])
				
	if len(fileList)>0:
		print ("\n Available files:")
		for number, item in enumerate(fileList):
			print ("\t{}\t{}".format(number+1, ".".join(item[:2])))
		choice = raw_input("Choose a file (enter 0 to abort): ")
		while True:
			try:
				choice = int(choice)
				if choice == 0: return
			except ValueError:
				choice = int(raw_input("Invalid input. Please select a file or enter '0' to quit."))
			else:
				selectedFile = fileList[choice-1]
				print("File '"+ selectedFile[0]+"."+selectedFile[1]+"' selected.\n")
				return "{2}{0}.{1}".format(*selectedFile)

			
	else:
		raw_input("No files found in folder 'raw'. Please check folder and try again\nPress any key to exit...")
		return

def getAllFiles():
	filelist=[]
	for root, sub, files in os.walk("./raw/"):
		for filename in files:
			_filename, ext = os.path.splitext(filename)
			if ext[1:]=='gb':
				pathname=os.path.join(root, filename)
				filelist.append(pathname)
				print pathname
	print("Finished browsing folder 'raw'. {} .gb files were found.".format(len(filelist)))
	return filelist

class geneFunctions():
	def __init__(self):
		self.options = {"Batch-merge all files in 'raw' sub-folder":'mergeAllFiles', "Make a file with multiple entries (e.g. .gbff) Artemis-compatible through inserting a spacer":'processMultiFile', "Quit":'exit'}
		
	def mergeFiles(self, fileA, fileB):
		"""This function merges two GenBank formatted files into one, without preserving IDs or descriptions."""
		_fileA = SeqIO.read(fileA, "genbank") 
		_fileB = SeqIO.read(fileB, "genbank") 
		_fileCombined = _fileA + ("N" * 6) + _fileB 
		return _fileCombined
		
	#this is dumb
	def mergeAllFiles(self):
		allFiles = getAllFiles()
		allFiles = map(lambda x: SeqIO.read(x, "genbank"), allFiles)
		masterFile = allFiles.pop()
		for num, file in enumerate(allFiles):
			print("Processing file #{}, {}...".format(num, file.id))
			masterFile = masterFile + "N"*6 + file
		name=raw_input("Please enter a filename for the output: ")
		SeqIO.write(masterFile, "./output/{}.gbk".format(name), "genbank") 
		print("Merger completed successfully; {} files merged. Result saved as {}.gbp.".format(len(allFiles)+1, name))
			
	def exit(self):
		return
		
	def processMultiFile(self):	
		merged_rec = ''
		infile = pickOneFile("raw")
		infile = SeqIO.parse(open(infile,"r"), "genbank")
		c = 1
		for rec in infile:
			print("Processing entry {}...".format(c))
			#optional spacer
			_rec = rec + ("N"*6)
			merged_rec += _rec 
			c+=1
			
		merged_rec.id = "mergedseq"
		merged_rec.description = "merged seq"
		name=raw_input("Please enter a filename for the output: ")
		SeqIO.write(merged_rec, "./output/{}.gbk".format(name), "genbank") 
		print("Process completed successfully. Result saved as {}.gbp.".format(name))
		
if __name__ == "__main__":
	mainMenu()
	raw_input("Press enter key to exit...")
