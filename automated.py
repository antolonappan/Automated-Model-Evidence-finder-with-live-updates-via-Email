import os
import glob
import numpy as np
import sys
MOD='/home/pilonppan/Evidence/modules/'
sys.path.insert(0, MOD)
from mymail import *

models=glob.glob('models/*')
lcdm=models.index('models/LCDM')
model0=models[0]
models[0]=models[lcdm]
models[lcdm]=model0

model_path = models


comb={1:'BAO+SL+H0',
      2:'BAO+SL+H',
      3:'BAO+SL+H+JLA',
      4:'BAO+SL+H+JLA+CMB',
      5:'BAO+SL+H+JLA+CMB+GROWTH'}

one_time_switch = 0

for model in model_path:
     evi=[]
     for combination in range(1,6):
           print('Running %s with combination %s'%(model[7:],comb[combination]))
           os.system('mpiexec -n 15 python %s/multinest.py %i'%(model,combination))
  
           datadir = comb[combination]
           with open('%s/%s/stats.dat'%(model,datadir)) as file:
                 lines =file.readlines()
                 line = lines[0]
           evi.append(float(line[50:75]))

     if one_time_switch == 0:
           reference_evidence = evi
           one_time_switch =1
     
     bf= list(np.array(evi)-np.array(reference_evidence))
     message = """BAO+SL+H0                     ={0}     {5}\nBAO+SL+H                     ={1}     {6}\nBAO+SL+H+JLA                ={2}     {7}\nBAO+SL+H+JLA+CMB        ={3}     {8}\nBAO+SL+H+JLA+CMB+GROWTH ={4}     {9}\n""".format(evi[0],evi[1],evi[2],evi[3],evi[4],bf[0],bf[1],bf[2],bf[3],bf[4])
     subject = "Results of %s"%model[7:]
     send(["antoidicherian@gmail.com","pilonppan@gmail.com"],subject,message)
     
