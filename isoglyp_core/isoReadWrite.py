def readFastaFile(filename):
   f = open(filename,'r')
   lines = f.readlines()
   f.close()

   sc = list("1234567890[];:<,.?\'\"\ ")

   numlines = len(lines)
   i=0
   results = []
   name = ''
   seq = ''
   boo = 0
   while i < numlines:
      if boo == 0 and lines[i][0] == '>':
         name = lines[i].strip()
         boo = 1
      elif boo == 1 and lines[i][0] == '>':
         results.append([name,seq])
         name = lines[i].strip()
         seq = ''
      else:
         for ch in sc:
            if ch in lines[i]:
               lines[i] = lines[i].replace(ch,'')
         seq = seq + lines[i].strip().strip(u'\u200b').upper()
      i = i +1
   if boo == 1:
      results.append([name,seq])

   return results
   
def readAccessionFile(filename):
	import urllib.request, urllib.parse, urllib.error, time
	f1=open(filename,'r')
	lines = f1.readlines()
	f1.close()
	processed = []
	results = []
	redo = []
	for i in lines:
		
		itrim=i.strip()
		if itrim == "" or itrim in processed:
			continue
		else:
			print(itrim)
			try:
				localfile=urllib.request.urlopen('http://www.uniprot.org/uniprot/'+itrim+'.fasta')
				temp=localfile.readlines()
				res=''
				for i in range(1,len(temp)):
					res=res+temp[i].decode("utf-8").strip()
				processed.append(itrim)
				results.append([">"+itrim,res])
			except:
				print('Sequence: %s could not be retrieved'%itrim)
				redo.append(itrim)
		if len(processed)%10 == 0:
			time.sleep(5)
	for itrim in redo:
		print(itrim)
		if itrim == "" or itrim in processed:
			try:
				localfile=urllib.request.urlopen('http://www.uniprot.org/uniprot/'+itrim+'.fasta')
				temp=localfile.readlines()
				res=''
				for i in range(1,len(temp)):
					res=res+temp[i].decode("utf-8").strip()
				processed.append(itrim)
				results.append([">"+itrim,res])
			except:
				print('Sequence: %s could not be retrieved again'%itrim)
			time.sleep(5)
	return results
