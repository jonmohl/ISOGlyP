#! /usr/bin/python

import os
import re
import sys
import argparse
from numpy import random
import time

OUTPUT_DIR = ''

from Config import *

#fileIn=open(,'r')
out_run = str(time.time())

workdir = os.getcwd()

abspath = os.path.dirname(__file__)

if abspath == '':
   abspath = '.'

sys.path.append(abspath)

os.chdir(abspath)

#Setting Defaults
cscore = 1
tscore = 1

ran = 0
seq = 0
cs = 0
seed = ''

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fasta', type=str)
parser.add_argument('-j', '--jobId', type=str)
parser.add_argument('-ts', '--thrser', type=str)
parser.add_argument('-pc', '--positive_cutoff', type=float, default=1.1)
parser.add_argument('-nc', '--negative_cutoff', type=float, default=0.8)
parser.add_argument('-pos', '--positive_trans', type=str)
parser.add_argument('-neg', '--negative_trans', type=str)
parser.add_argument('-iter', '--iterations', type=int, default=10000)
parser.add_argument('-num', '--num_petides', type=int, default=50)
parser.add_argument('-evt', '--enhance_val_table_dir', type=str, default=EVT_ROOT)
parser.add_argument('-posi', '--positions', type=str)
parser.add_argument('-rat', '--ratio', type=str)
parser.add_argument('-s', '--seed',type=str)
parser.add_argument('-ex','--exclude',type=str)
parser.add_argument('-cs','--core_sequence',type=str)

args = parser.parse_args()

if args.fasta:
   fileIn = args.fasta
   seq = 1
elif args.core_sequence:
   core_sequence = list(args.core_sequence)
   cs = 1
else:
   ran = 1


if args.jobId:
   jobId = args.jobId
else:
   jobId = out_run

if args.thrser:
   if args.thrser == 'T' or args.thrser == 't':
      core = 0
   elif args.thrser == 'S' or args.thrser == 's':
      core = 1
   elif args.thrser == 'B' or args.thrser == 'b':
      core = 2
   else:
      print('Error: -st needs to be either, S,T or B')
      exit()
else:
   core = 0

if not OUTPUT_DIR:
   outdir = './'
else:
   outdir = OUTPUT_DIR + '/' + jobId

if args.seed:
   seed = args.seed.split('.')[0]
else:
   seed = jobId.split('.')[0]

if args.exclude:
	exclude_list = args.exclude.split(',')
else:
	exclude_list = []


ev_dir = args.enhance_val_table_dir

positive_cutoff = float(args.positive_cutoff)
negative_cutoff = float(args.negative_cutoff)
numPeptides = int(args.num_petides)

if args.iterations:
   iterations = args.iterations


pos_trans='1,1,0,0,0,0,0,0,0,0,0,1'
neg_trans='0,0,1,0,0,0,0,0,0,0,0,1'

pos_transferases = []
pos_transferases = pos_trans.split(',')
neg_transferases = []
neg_transferases = neg_trans.split(',')

if args.positive_trans:
   pos_transferases = args.positive_trans.split(',')
   #pos_transferases.append('1')
if args.negative_trans:
   neg_transferases = args.negative_trans.split(',')
   #neg_transferases.append('1')

if args.positions:
   posi = args.positions
else:
   posi='0,0,0,1,1,1,1,1,1,0,0,0'
positions = []
positions = positions + [int(pos) for pos in posi.split(',')]

if args.ratio:
   ratio = args.ratio
else:
   ratio='15.1,6.61,15.6,2.8,8.01,3.0,8.15,2.5,14.5,6.48,6.35'

sweight = []
sweight = [float(swei) for swei in ratio.split(',')]

#List of amino acids available for peptides
AA_list = ['A','D','E','F','G','H','I','K','L','M','N','P','Q','R','V','Y']
for e in exclude_list:
   if e in AA_list:
      AA_list.remove(e)

pos_scores = {}
neg_scores = {}

if ran == 1:
   #Create weights for position specific
   weights = []
   for m in range(0,len(AA_list)):
      weights.append(float(1.00000/len(AA_list)))

   #create list of random peptides
   peptides = []
   #st = time.time()
   for n in range(0,iterations):
      if seed:
         random.seed(int(float(seed.split('_')[0]))+n)
      else:
         random.seed(int(float(jobId.split('_')[0]))+n)
      temp = ''
      for n in range(1,6):
         if positions[n] == 1:
            temp = temp + random.choice(AA_list,1,p=weights,replace=False)[0]
         else:
            temp = temp + '-'
      if core == 0:
         temp = temp + 'T'
      elif core == 1:
         temp = temp + 'S'
      else:
         temp = temp + random.choice(['S','T'])[0]

      for n in range(6,11):
         if positions[n] == 1:
            temp = temp + random.choice(AA_list,1,p=weights,replace=False)[0]
         else:
            temp = temp + '-'
      if temp not in peptides:
         peptides.append(temp)
   #print('Peptide creation time: %0.4fs'%(time.time()-st))
   #st = time.time()
   for n in peptides:
      psc = isoglyp_core.isoResults.constructResults(n, positions[1:11], pos_transferases, cscore, tscore, sweight, ev_dir)
      pos_scores[n] = psc[0][-1]
      nsc = isoglyp_core.isoResults.constructResults(n, positions[1:11], neg_transferases, cscore, tscore, sweight, ev_dir)
      neg_scores[n] = nsc[0][-1]
   #print('Prediction time: %0.4fs'%(time.time()-st))

elif cs == 1:
   #Create weights for position specific
   weights = []
   for m in range(0,len(AA_list)):
      weights.append(float(1.00000/len(AA_list)))

   #Prepare core_sequence
   if 'T' in core_sequence:
      center = core_sequence.index('T')
   elif 'S' in core_sequence:
      center = core_sequence.index('S')
   else:
      print('No T or S to make as the center. Please resubmit!')
      exit()
   if center < 5:
      for x in range(0,5-center):
         core_sequence = ['-'] + core_sequence
         center += 1
   if len(core_sequence)-center < 6:
      for x in range(len(core_sequence)-center,12):
         core_sequence.append('-')
   core_sequence = core_sequence[(center-5):(center+6)]
   #create list of random peptides to fill in X on sequence
   peptides = []
   for n in range(0,iterations):
      if seed:
         random.seed(int(float(seed.split('_')[0]))+n)
      else:
         random.seed(int(float(jobId.split('_')[0]))+n)
      temp = ''
      for n in range(1,6):
         if positions[n] == 1 and core_sequence[n-1] == 'X':
            temp = temp + random.choice(AA_list,1,p=weights,replace=False)[0]
         else:
            temp = temp + core_sequence[n-1]

      temp = temp + core_sequence[5]
      for n in range(6,11):
         if positions[n] == 1 and core_sequence[n] == 'X':
            temp = temp + random.choice(AA_list,1,p=weights,replace=False)[0]
         else:
            temp = temp + core_sequence[n]

      if temp not in peptides:
         peptides.append(temp)

   for n in peptides:
      psc = isoglyp_core.isoResults.constructResults(n, positions[1:11], pos_transferases, cscore, tscore, sweight, ev_dir)
      pos_scores[n] = psc[0][-1]
      nsc = isoglyp_core.isoResults.constructResults(n, positions[1:11], neg_transferases, cscore, tscore, sweight, ev_dir)
      neg_scores[n] = nsc[0][-1]


elif seq == 1:
   sequences = isoglyp_core.isoReadWrite.readFastaFile('%s'%(fileIn))
   #create list of seq peptides
   peptides = []
   names = {}
   for sequence in sequences:
      header = sequence[0].split()[0][1:]
      ind = [m.start() for m in re.finditer('[ST]',sequence[1])]
      for n in ind:
         toSubmit = ''
         if n < 5:
            for p in range(0,5-n):
               toSubmit = toSubmit + '-'
            toSubmit = toSubmit + sequence[1][0:n+6]
         elif n+6 > len(sequence[1]):
            toSubmit = sequence[1][n-5:len(sequence[1])]
            for p in range(len(toSubmit),11):
               toSubmit = toSubmit + '-'
         else:
            toSubmit = sequence[1][n-5:n+6]
         if (toSubmit[5] == 'T' and core == 0) or core == 2:
            peptides.append(toSubmit)
            name = header+'_'+str(n+1)
            names[name] = toSubmit
         elif (toSubmit[5] == 'S' and core == 1) or core == 2:
            peptides.append(toSubmit)
            name = header+'_'+str(n+1)
            names[name] = toSubmit

   for n in names.keys():
      psc = isoglyp_core.isoResults.constructResults(names[n], positions[1:11], pos_transferases, cscore, tscore, sweight, ev_dir)
      nsc = isoglyp_core.isoResults.constructResults(names[n], positions[1:11], neg_transferases, cscore, tscore, sweight, ev_dir)
      temp = []
      i = 0
      while i <= len(psc):
         if psc[i][0] == 5:
            pos_scores[n] = psc[i][-1]
            neg_scores[n] = nsc[i][-1]
            i+=15
         i+=1


#st = time.time()
pep_sorted = sorted(pos_scores, key=pos_scores.__getitem__, reverse=True)
#print('Peptide sorting time: %0.4fs'%(time.time()-st))
i = 0
j = 0

f = open('%s/isoglyp-%s.csv'%(outdir,jobId), 'w')
if seq == 1:
   f.write('Peptides generated from %s file\n'%fileIn)
if ran == 1:
   f.write('Peptides chosen from %s randomly generated.\n'%iterations)
if cs == 1:
   f.write('%s randomly generated peptides using the sequence %s as a framwork.\n'%(iterations,''.join(core_sequence)))
f.write('Enhancement Value Version: %s\n'%ev_dir.split('\')[-1])
f.write('Seed used in random number generator: %s\n'%seed)
f.write(',T1,T2,T3,T4,T5,T10,T11,T12,T13,T14,T16\n')
f.write('Selected-For,%s\n'%(','.join(pos_transferases[:-1])))
f.write('Selected-Against,%s\n'%(','.join(neg_transferases[:-1])))
f.write('Thr/Ser Ratio,%s\n'%ratio)
f.write('Positions,%s,X,%s\n'%(','.join(posi.split(',')[1:6]),','.join(posi.split(',')[6:11])))

ss = 1
while positions[ss] != 1:
   ss+=1
ss -= 1
st = 11
while positions[st] != 1:
   st-=1
st+=1
if ran == 1 or cs ==1:
   f.write('Peptide Number,Sequence,Positive EVP,Negative EVP\n')
   while i < numPeptides and j < len(peptides) and float(pos_scores[pep_sorted[j]]) > positive_cutoff:
      if neg_scores[pep_sorted[j]] < negative_cutoff:
         f.write('%s,%s,%s,%s\n'%(str(i+1),pep_sorted[j][ss:st], str(pos_scores[pep_sorted[j]]),str(neg_scores[pep_sorted[j]])))
         i+=1
      j+=1

else:
   f.write('Protein Name & Location,Sequence,Positive EVP,Negative EVP\n')
   while float(pos_scores[pep_sorted[j]]) > positive_cutoff:
      if neg_scores[pep_sorted[j]] < negative_cutoff:
         f.write('%s,%s,%s,%s\n'%(pep_sorted[j],names[pep_sorted[j]], str(pos_scores[pep_sorted[j]]),str(neg_scores[pep_sorted[j]])))
         i+=1
      j+=1


f.close()
print('Completed')
