def constructResults(seq, pos, transferases, cscore, tscore, sweight, ev_dir):
   import re
   from isoEVPCalc import basicEVP
   from isoEVPCalc import preExtEVP
   from isoEVPtables import returnEVTable
   
   #create index of TS's within the sequence
   ind = [m.start() for m in re.finditer('[ST]',seq)]

   toReturn = []

   if len(seq) < 12:
      for n in range(len(seq),12):
        seq = seq + '-'

   for m in ind:
      toSubmit = ''
      if m < 5:
         for n in range(0,5-m):
            toSubmit = toSubmit + '-'
         toSubmit = toSubmit + seq[0:m+6]
      elif m+6 > len(seq):
         toSubmit = seq[m-5:len(seq)]
         for n in range(len(toSubmit),11):
            toSubmit = toSubmit + '-'
      else:
         toSubmit = seq[m-5:m+6]

      toReturnScores = []
      
      toReturnScores.append(m)
      toReturnScores.append(toSubmit)
      max = -100

      #Determine if the site of interest has a upstream or downstream prior potential glycosylation effect
      start = m - 15
      if start < 0:
         start = 0
      end = m - 5
      if end < 0:
         end = 0
      ex_neg_len = len([n.start() for n in re.finditer('[ST]',seq[start:end])])

      start = m - 5
      if start < 0:
         start = 0
      cl_neg_ind = [n.start() for n in re.finditer('[ST]',seq[start:m])]

      end = m + 15
      if end > len(seq):
         end = len(seq)-1
      start = m+5
      if start > len(seq):
         start = len(seq)-1
      ex_pos_len = len([n.start() for n in re.finditer('[ST]',seq[start:end])])

      end = m + 5
      if end > len(seq):
         end = len(seq)-1
      cl_pos_ind = [n.start() for n in re.finditer('[ST]',seq[(m+1):end])]

      #GalNAc T1
      if transferases[0] != '0':
         if ex_neg_len > 0:
            toReturnScores.append('0')
         else:
            toReturnScores.append('0')
         if len(cl_neg_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         #dict = returnDict('T1')
         dict = returnEVTable('%s.T1.csv'%ev_dir)
         if cscore == 0:
            dict['C'] = dict['S']
         if tscore == 0:
            dict['T'] = dict['S']
         score = preExtEVP(toSubmit, pos,dict)
         if toSubmit[5] == 'S':
            score = score / sweight[0]
         toReturnScores.append(score)
         if score > max:
            max = score
         if len(cl_pos_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         if ex_pos_len > 0:
            toReturnScores.append('1')
         else:
            toReturnScores.append('0')
      else:
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')

      #GalNAc T2
      if transferases[1] != '0':
         if ex_neg_len > 0:
            toReturnScores.append('0')
         else:
            toReturnScores.append('0')
         if len(cl_neg_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         #dict = returnDict('T2')
         dict = returnEVTable('%s.T2.csv'%ev_dir)
         if cscore == 0:
            dict['C'] = dict['S']
         if tscore == 0:
            dict['T'] = dict['S']
         score = preExtEVP(toSubmit, pos,dict)
         if toSubmit[5] == 'S':
            score = score / sweight[1]
         toReturnScores.append(score)
         if score > max:
            max = score
         if len(cl_pos_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         if ex_pos_len > 0:
            toReturnScores.append('1')
         else:
            toReturnScores.append('0')
      else:
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')


      #GalNAc T3
      if transferases[2] != '0':
         if ex_neg_len > 0:
            toReturnScores.append('1')
         else:
            toReturnScores.append('0')
         if len(cl_neg_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         #dict = returnDict('T3')
         dict = returnEVTable('%s.T3.csv'%ev_dir)
         if cscore == 0:
            dict['C'] = dict['S']
         if tscore == 0:
            dict['T'] = dict['S']
         score = preExtEVP(toSubmit, pos,dict)
         if toSubmit[5] == 'S':
            score = score / sweight[2]
         toReturnScores.append(score)
         if score > max:
            max = score
         if len(cl_pos_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         if ex_pos_len > 0:
            toReturnScores.append('0')
         else:
            toReturnScores.append('0')
      else:
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')


      #GalNAc T4
      if transferases[3] != '0':
         if ex_neg_len > 0:
            toReturnScores.append('1')
         else:
            toReturnScores.append('0')
         if len(cl_neg_ind) > 0:
            toReturnScores.append('1')
         else:
            toReturnScores.append('0')
         #dict = returnDict('T3')
         dict = returnEVTable('%s.T4.csv'%ev_dir)
         if cscore == 0:
            dict['C'] = dict['S']
         if tscore == 0:
            dict['T'] = dict['S']
         score = preExtEVP(toSubmit, pos,dict)
         if toSubmit[5] == 'S':
            score = score / sweight[2]
         toReturnScores.append(score)
         if score > max:
            max = score
         if len(cl_pos_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         if ex_pos_len > 0:
            toReturnScores.append('0')
         else:
            toReturnScores.append('0')
      else:
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')


      #GalNAc T5
      if transferases[4] != '0':
         if ex_neg_len > 0:
            toReturnScores.append('1')
         else:
            toReturnScores.append('0')
         if len(cl_neg_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         #dict = returnDict('T5')
         dict = returnEVTable('%s.T5.csv'%ev_dir)
         if cscore == 0:
            dict['C'] = dict['S']
         if tscore == 0:
            dict['T'] = dict['S']
         score = preExtEVP(toSubmit, pos,dict)
         if toSubmit[5] == 'S':
            score = score / sweight[3]
         toReturnScores.append(score)
         if score > max:
            max = score
         if len(cl_pos_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         if ex_pos_len > 0:
            toReturnScores.append('1')
         else:
            toReturnScores.append('0')
      else:
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')


      #GalNAc T10
      if transferases[5] != '0':
         if ex_neg_len > 0:
            toReturnScores.append('0')
         else:
            toReturnScores.append('0')
         if len(cl_neg_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         #dict = returnDict('T10')
         dict = returnEVTable('%s.T10.csv'%ev_dir)
         if cscore == 0:
            dict['C'] = dict['S']
         if tscore == 0:
            dict['T'] = dict['S']
         score = preExtEVP(toSubmit, pos,dict)
         if toSubmit[5] == 'S':
            score = score / sweight[4]
         toReturnScores.append(score)
         if score > max:
            max = score
         if 0 in cl_pos_ind:
            toReturnScores.append('1')
         else:
            toReturnScores.append('0')
         if ex_pos_len > 0:
            toReturnScores.append('0')
         else:
            toReturnScores.append('0')
      else:
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')

      #GalNAc T11
      if transferases[6] != '0':
         if ex_neg_len > 0:
            toReturnScores.append('0')
         else:
            toReturnScores.append('0')
         if len(cl_neg_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         #dict = returnDict('T11')
         dict = returnEVTable('%s.T11.csv'%ev_dir)
         if cscore == 0:
            dict['C'] = dict['S']
         if tscore == 0:
            dict['T'] = dict['S']
         score = preExtEVP(toSubmit, pos,dict)
         if toSubmit[5] == 'S':
            score = score / sweight[5]
         toReturnScores.append(score)
         if score > max:
            max = score
         if len(cl_pos_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         if ex_pos_len > 0:
            toReturnScores.append('0')
         else:
            toReturnScores.append('0')
      else:
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')


      #GalNAc T12
      if transferases[7] != '0':
         if ex_neg_len > 0:
            toReturnScores.append('1')
         else:
            toReturnScores.append('0')
         if len(cl_neg_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         #dict = returnDict('T12')
         dict = returnEVTable('%s.T12.csv'%ev_dir)
         if cscore == 0:
            dict['C'] = dict['S']
         if tscore == 0:
            dict['T'] = dict['S']
         score = preExtEVP(toSubmit, pos,dict)
         if toSubmit[5] == 'S':
            score = score / sweight[6]
         toReturnScores.append(score)
         if score > max:
            max = score
         if 2 in cl_pos_ind:
            toReturnScores.append('1')
         else:
            toReturnScores.append('0')
         if ex_pos_len > 0:
            toReturnScores.append('0')
         else:
            toReturnScores.append('0')
      else:
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')


      #GalNAc T13
      if transferases[8] != '0':
         if ex_neg_len > 0:
            toReturnScores.append('1')
         else:
            toReturnScores.append('0')
         if len(cl_neg_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         #dict = returnDict('T13')
         dict = returnEVTable('%s.T13.csv'%ev_dir)
         if cscore == 0:
            dict['C'] = dict['S']
         if tscore == 0:
            dict['T'] = dict['S']
         score = preExtEVP(toSubmit, pos,dict)
         if toSubmit[5] == 'S':
            score = score / sweight[7]
         toReturnScores.append(score)
         if score > max:
            max = score
         if len(cl_pos_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         if ex_pos_len > 0:
            toReturnScores.append('1')
         else:
            toReturnScores.append('0')
      else:
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')


      #GalNAc T14
      if transferases[9] != '0':
         if ex_neg_len > 0:
            toReturnScores.append('0')
         else:
            toReturnScores.append('0')
         if len(cl_neg_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         #dict = returnDict('T14')
         dict = returnEVTable('%s.T14.csv'%ev_dir)
         if cscore == 0:
            dict['C'] = dict['S']
         if tscore == 0:
            dict['T'] = dict['S']
         score = preExtEVP(toSubmit, pos,dict)
         if toSubmit[5] == 'S':
            score = score / sweight[8]
         toReturnScores.append(score)
         if score > max:
            max = score
         if len(cl_pos_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         if ex_pos_len > 0:
            toReturnScores.append('1')
         else:
            toReturnScores.append('0')
      else:
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         

      #GalNAc T16
      if transferases[10] != '0':
         if ex_neg_len > 0:
            toReturnScores.append('1')
         else:
            toReturnScores.append('0')
         if len(cl_neg_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         #dict = returnDict('T16')
         dict = returnEVTable('%s.T16.csv'%ev_dir)
         if cscore == 0:
            dict['C'] = dict['S']
         if tscore == 0:
            dict['T'] = dict['S']
         score = preExtEVP(toSubmit, pos,dict)
         if toSubmit[5] == 'S':
            score = score / sweight[9]
         toReturnScores.append(score)
         if score > max:
            max = score
         if len(cl_pos_ind) > 0:
            toReturnScores.append('-1')
         else:
            toReturnScores.append('0')
         if ex_pos_len > 0:
            toReturnScores.append('1')
         else:
            toReturnScores.append('0')
      else:
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')
         toReturnScores.append('-')

      if transferases[11] != '0':
         toReturnScores.append(max)
      else:
         toReturnScores.append('-')

      toReturn.append(toReturnScores)
         
   return toReturn

