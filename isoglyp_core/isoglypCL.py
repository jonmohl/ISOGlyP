#! /usr/bin/python

import os
import re
import sys
import argparse

workdir = os.getcwd()

abspath = os.path.dirname(__file__)

if abspath == '':
   abspath = '.'

sys.path.append(abspath)


import isoEVPtables
import isoReadWrite
import isoResults

os.chdir(abspath)

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fasta', type=str)
parser.add_argument('-p', '--parameters', type=str)
parser.add_argument('-j', '--jobId', type=str)
parser.add_argument('-c', '--cutoff', type=str)

args = parser.parse_args()

fileIn = args.fasta
parIn = args.parameters
if args.jobId:
   jobId = args.jobId
else:
   jobId = 'null'

if args.cutoff:
   cutoff = args.cutoff
else:
   cutoff = 1

sequences = isoReadWrite.readFastaFile('%s'%(fileIn))

para = open('%s'%(parIn), 'r')
parLines = para.readlines()
para.close()

cscore = 1
tscore = 1

out_path = '/'.join(parIn.split('/')[0:-1])

for line in parLines:
   if re.search('^pos',line):
      positions = []
      positions = positions + [int(pos) for pos in line.strip().split('=')[1].split(',')]


   if re.search('^trans', line):
      transferases = []
      transferases = line.strip().split('=')[1].split(',')

   if re.search('^ratio',line):
      sweight = []
      sweight = [float(swei) for swei in line.strip().split('=')[1].split(',')]

   if re.search('^cscore',line):
      cscore=line.strip().split('=')[1]

   if re.search('^tscore',line):
      tscore=line.strip().split('=')[1]

   if re.search('^evd',line):
      ev_dir = line.strip().split('=')[1]

resultsCSV = ''
resultsCSV = resultsCSV + '#O-glycosylation Prediction from ISOGlyP.utep.edu\n'
resultsCSV = resultsCSV + '#EV Table Version: %s\n'%ev_dir.split('/')[-1]
resultsCSV = resultsCSV + '#Positions used in Calculation: %s\n'%(' '.join('%s'%pos for pos in positions))
resultsCSV = resultsCSV + '#Thr/Ser Ratio: %s\n'%sweight

resultsCSV = resultsCSV + ','.join(['Sequence Name', 'S/T', 'Position', 'Pattern', 'Extended','Extended','T1','Extended','Extended','Extended','Extended','T2','Extended','Extended','Extended','Extended', 'T3','Extended','Extended','Extended','Extended', 'T4','Extended','Extended','Extended','Extended','T5','Extended','Extended','Extended','Extended','T10','Extended','Extended','Extended','Extended','T11','Extended','Extended','Extended','Extended','T12','Extended','Extended','Extended','Extended','T13','Extended','Extended','Extended','Extended','T14','Extended','Extended','Extended','Extended','T16','Extended','Extended','Max']) + '\n'

count = 0

for n in sequences:
   scores = isoResults.constructResults(n[1], positions[1:11], transferases, cscore, tscore, sweight, ev_dir)
   for m in scores:
      resultsCSV = resultsCSV + n[0].replace(',','') + ',' + m[1][5] + ',' + str(m[0]+1) + ',' + ','.join(str(m[x]) for x in range(1,len(m))) + '\n'
   count += 1
   if count%20 == 0:
      log = open('%s/%s.log'%(out_path,('%s'%jobId).split('.')[0]), 'a')
      log.write('Processed %s of %s sequences...\n'%(count,len(sequences)))
      log.close()

f = open('%s/isoglyp-%s.csv'%(out_path, jobId), 'w')
f.write(resultsCSV)
log = open('%s/%s.log'%(out_path,('%s'%jobId).split('.')[0]), 'a')
log.write('Completed')
log.close()
