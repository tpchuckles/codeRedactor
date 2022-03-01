import sys


functionBlacklist=[]

keywordsToRedact=[]

fileIn,fileOut=sys.argv[1:3]

lines=open(fileIn,'r').readlines()		# read all lines of the input file

# PURGING ENTIRE FUNCTIONS FROM THE CODE
for func in functionBlacklist:			# for each blacklisted function
	for i in range(len(lines)):		# look for this function in each line
		if "def "+func in lines[i]:	# if we find the function declaration, record line's index
			break

	for j in range(i,-1,-1):		# walk up in the file, looking for pre-function stuff (wrappers, glos declared outside the function, etc)
		l="".join(lines[j].split())	# purge whitespace
		if len(l)==0:			# empty line found above the function? stop walking
			j=j+1			# (we don't actually want to delete empty line)
			break

	for k in range(i+1,len(lines)):		# walk down in the file, looking for beginning of the next function
		l=lines[k]
		if len(l)>0 and l[0] not in ["\t"," ","\n"]: # next function or outside-of-function code won't start with a tab, space, or be empty newline
			k=k-1			# (this line had next stuff, so leave it. previous line will be last one to remove)
			break
	for k in range(k,i,-1):			# walk *back up*, ignoring empty lines
		l="".join(lines[k].split())
		if len(l)!=0:
			break

	#print(lines[j:k+1])
	lines=lines[:j]+lines[k+1:]

# JUST A BASIC "FIND AND REPLACE" FOR BANNED KEYWORDS
for i,line in enumerate(lines):			# loop through lines
	for key in keywordsToRedact:		# replace each keyword
		line=line.replace(key,"[REDACTED]")
	lines[i]=line

with open(fileOut,'w') as f:
	for l in lines:
		f.write(l)

