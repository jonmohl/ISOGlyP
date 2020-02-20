def returnHTMLtable(fi, trans):
   if trans == '':
      return ''
   print(fi)
   
   Tdict = returnEVTable(fi)

   keyIndex = ['A','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','V','Y','X','+','$','T','C','W']

   toReturn = "<br><strong><h2>" + trans + "</h2></strong>"

   toReturn = toReturn + "EVT Version: " + fi.split('/')[-1].split('.')[-3] + "<br>\n"

   toReturn = toReturn + "TS Ratio: " + TSratio('.'.join(fi.split('.')[0:-2])+'.ts.csv',trans) + "<br>\n"

   toReturn = toReturn + "<table border='1' cellpadding='3' cellspacing='3' width='100%'>\
      <tr>\
      <td>&nbsp;</td><td><center><strong>-5</strong></center></td><td><center><strong>-4</strong></center></td><td><center><strong>-3</strong></center></td>\
      <td><center><strong>-2</strong></center></td><td><center><strong>-1</strong></center></td><td><center><strong>0</strong></center></td>\
      <td><center><strong>+1</strong></center></td><td><center><strong>+2</strong></center></td><td><center><strong>+3</strong></center></td>\
      <td><center><strong>+4</strong></center></td><td><center><strong>+5</strong></center></td>\
      </tr>\
      <tr><td style='border: 1px solid #00033; ' align='center'>"

   el = estList(trans)

   for i in keyIndex:
      if i in el:
         toReturn = toReturn + '<tr><td><font color=\'#FF0000\'><center><strong>' + i + '</strong></center></font></td>'
         for n in range(1,6):
            toReturn = toReturn + '<td><font color=\'#FF0000\'><center>' + str(Tdict[i][n]) + '</center></font></td>'
         toReturn = toReturn + '<td>&nbsp;</td>'
         for n in range(6,11):
            toReturn = toReturn + '<td><font color=\'#FF0000\'><center>' + str(Tdict[i][n]) + '</center></font></td>'
         toReturn = toReturn + '</tr>'
      else:
         toReturn = toReturn + '<tr><td><center><strong>' + i + '</strong></center></td>'
         for n in range(1,6):
            toReturn = toReturn + '<td><center>' + str(Tdict[i][n]) + '</center></td>'
         toReturn = toReturn + '<td>&nbsp;</td>'
         for n in range(6,11):
            toReturn = toReturn + '<td><center>' + str(Tdict[i][n]) + '</center></td>'
         toReturn = toReturn + '</tr>'

   toReturn = toReturn + '</table>'

   return toReturn
      
def returnEVTable(fi):
   f = open(fi,'r')
   lines = f.readlines()
   f.close()

   trans = {}
   for line in lines[1:]:
      sl = line.split(',')
      temp = [sl[1]]
      for n in sl[2:-1]:
         temp.append(float(n))
      temp.append(sl[-1].strip())
      trans[sl[0]] = temp
   return trans

def estList(trans):
   #Used to return which values are estimated
   if trans == 'T1':
      return ['C', 'T', 'X', 'W']

   if trans == 'T2':
      return ['C', 'T', 'X', 'W']

   if trans == 'T3':
      return ['C', 'T', 'X', '+', '$', 'W']

   if trans == 'T4':
      return ['C', 'T', 'X', '+', '$', 'W']

   if trans == 'T5':
      return ['C', 'T', 'X', '+', '$', 'W']

   if trans == 'T10':
      return ['C', 'T', 'X', 'W']

   if trans == 'T11':
      return ['C', 'T', 'X', '+', '$', 'W']

   if trans == 'T12':
      return ['C', 'T', 'X', '+', '$', 'W']

   if trans == 'T13':
      return ['C', 'T', 'X', '+', '$', 'W']

   if trans == 'T14':
      return ['C', 'T', 'X', '+', '$', 'W']

   if trans == 'T16':
      return ['C', 'T', 'X', '+', '$', 'W']

   return []


def TSratio(fi, trans):
   f = open(fi,'r')
   l = f.readlines()
   f.close()

   return(l[1].split(',')[l[0].split(',').index(trans)])
