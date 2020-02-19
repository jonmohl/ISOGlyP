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
