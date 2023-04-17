import re
from shutil import copyfile
from pathlib import Path
import h5py
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
import sys

## Sensitivity Analysis Library ###
from SALib.sample import saltelli, latin
from SALib.analyze import sobol
from SALib.test_functions import Ishigami

from IMF_calculations import *

plt.rcParams['xtick.labelsize'] = 20         
plt.rcParams['ytick.labelsize'] = 20
plt.rcParams['xtick.major.size'] = 10
plt.rcParams['ytick.major.size'] = 10

plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['figure.figsize'] = (10,8)
plt.rcParams['font.size'] = 20
pd.set_option('display.max_columns', 500)

problem = {
    'num_vars': 14,
    'names': ['stabledisk', 'alphahot', 'alpha_cool', 'alpha_reheat',
              'vhotdisk', 'vhotburst', 'fellip', 'fburst', 'nu_sf', 'F_SMBH', 'tau_star_min_burst',
              'set fcloud', 'set tesc', 'set beta2_burst'],
    'bounds': [[0.5, 1.2],
               [1.0, 4.0],
               [0.2, 2.0],
               [0.2, 2.0],
               [10, 800],
               [10, 800],
               [0.2, 0.5],
               [0.01, 0.3],
               [0.1, 3.0],
               [0.001, 0.05],
               [0.01, 0.5],
	           [1.0, 3.0],
               [0.2, 0.8],
               [0.001, 0.010],
               [1.5, 2.0]]
}
params =  np.load('/cosma5/data/durham/glfn88/current_params.npy')
retfrac_yields = []
IMF_params = params[:,11]
for param in IMF_params:
	retfrac_yield = gen_retfrac_yield(param-1) #Salpeter = 1.35
	retfrac_yields.append(retfrac_yield)
retfrac_yields = np.array(retfrac_yields) 
print(retfrac_yields)
param_values = np.load('/cosma5/data/durham/glfn88/current_params.npy')[:,:11]
dust_params = np.load('/cosma5/data/durham/glfn88/current_params.npy')[:, 12:]

basefile = '/cosma5/data/durham/glfn88/test_counts_chabrier.input.ref' # Original GALFORM input parameters file for the
# modified Lacey et al. (2016( model ).
run = '/cosma5/data/durham/glfn88/Galform_Out/v2.7.0/stable/L800'
# I don't think this run string does anything in this script.



for i, vals in enumerate(param_values):
    newName = '/cosma5/data/durham/glfn88/chabrier_wave1_optimization'+str(i)+'_expanded_range.input.ref'
    copyfile(basefile, newName) # Copy the contents of basefile into a new file with "newName" Modify newName without
    # modifying the base file
    with open(newName, 'r') as f:
        lines = f.readlines()
    with open(newName, 'w') as f:
        for k, line in enumerate(lines):
            written = 0 # Keeping track of how many lines are re-written
            for j, name in enumerate(problem['names'][:11]):
                if re.match(name+'(.*)', line):
                    written += 1

                    f.writelines(name +' = '+str(vals[j])+'\n')
            for j, name in enumerate(['burst_recycle', 'burst_yield']):
                if re.match(name+'(.*)', line):
                    written += 1; print(retfrac_yields[i,j])


                    f.writelines(name +' = '+str(retfrac_yields[i,j])+'\n')

            if written == 0:
                written += 1
                f.writelines(line)
    f.close()

#for i, vals in enumerate(retfrac_yields):
    #newName = '/cosma5/data/durham/glfn88/chabrier_wave1_optimization'+str(i)+'_expanded_range.input.ref'
    #copyfile(basefile, newName)
#    with open(newName, 'r') as f:
#        lines = f.readlines()
#    with open(newName, 'w') as f:
#        for k, line in enumerate(lines):
#            written = 0
#            for j, name in enumerate(['burst_recycle', 'burst_yield']):
#                if re.match(name+'(.*)', line):
#                    written += 1; print(vals[j])
#		    
#
#                    f.writelines(name +' = '+str(vals[j])+'\n')
#            if written == 0:
#                written += 1
#                f.writelines(line)
#    f.close()

for i, vals in enumerate(param_values):
	newName = '/cosma5/data/durham/glfn88/chabrier_wave1_optimization'+str(i)+'_expanded_range.input.ref'
	with open(newName, 'r') as f:
        	lines = f.readlines()
	with open(newName, 'w') as f:
		for k, line in enumerate(lines):
			if re.match('burst_seds'+'(.*)', line):
				f.writelines('burst_seds = [cw09v3.2_model_{}_Z0002, cw09v3.2_model_{}_Z0004, cw09v3.2_model_{}_Z0006, cw09v3.2_model_{}_Z0010, cw09v3.2_model_{}_Z0016, cw09v3.2_model_{}_Z0025, cw09v3.2_model_{}_Z0061, cw09v3.2_model_{}_Z0149, cw09v3.2_model_{}_Z0298]\n'.format(i,i,i,i,i,i,i,i,i))
			else:
				f.writelines(line)
	f.close()

                
                
basefile = '/cosma5/data/durham/glfn88/dustpars_Lacey16_10_hires.csh'
run = '/cosma5/data/durham/glfn88/Galform_Out/v2.7.0/stable/L800'
for i, vals in enumerate(dust_params):
    newName = '/cosma5/data/durham/glfn88/dustpars_chabrier_wave1_optimization'+str(i)+'_expanded_range.csh'
    copyfile(basefile, newName)
    tesc_counter=0
    with open(newName, 'r') as f:
        lines = f.readlines()
    with open(newName, 'w') as f:
        for k, line in enumerate(lines):
            written = 0
            for j, name in enumerate(problem['names'][11:]):
                if re.match(name+'(.*)', line):
                    written += 1
                    if name=='set tesc' and tesc_counter==0:
                        f.writelines(name+'_disk' +' = '+str(vals[j])+'\n')
                        tesc_counter+=1 
                    elif name=='set tesc' and tesc_counter==1:
                        f.writelines(name+'_burst' +' = '+str(vals[j])+'\n')
                    else:
                        f.writelines(name +' = '+str(vals[j])+'\n')
                    
            if written == 0:
                written += 1
                f.writelines(line)
    f.close()


                
                
runBasefile = '/cosma5/data/durham/glfn88/run_galform_counts.csh'
newNamerun = '/cosma5/data/durham/glfn88/run_galform_counts_chabrier_wave1.csh'

copyfile(runBasefile, newNamerun)

f = open(runBasefile, 'r')
contents = f.readlines()
f.close()
startline = 599
for i, vals in enumerate(param_values):
    contents.insert(startline+6*(i),  '# Chabrier wave1 param exploration #\n')
    contents.insert(startline+6*(i)+1, 'else if( $model == lc16.newmg.chabrier_wave1_optimization'+str(i)+'_expanded_range ) then\n')
    contents.insert(startline+6*(i)+2, '     set base_inputs_file = chabrier_wave1_optimization'+str(i)+'_expanded_range.input.ref\n')
    contents.insert(startline+6*(i)+3, '      cp $base_inputs_file $galform_inputs_file\n')
    contents.insert(startline+6*(i)+4, '      source dustpars_chabrier_wave1_optimization'+str(i)+'_expanded_range.csh\n')
    contents.insert(startline+6*(i)+5, '\n')

f = open(newNamerun, 'w')
contents = ''.join(contents)
f.write(contents)
f.close()

qsubBasefile = '/cosma5/data/durham/glfn88/qsub_trackdescendants.csh'
newNameqsub = '/cosma5/data/durham/glfn88/qsub_chabrier_wave1.csh'

subvols = 10
runscript = 'run_galform_counts_chabrier_wave1.csh'


copyfile(qsubBasefile, newNameqsub)

f = open(newNameqsub, 'r')
contents = f.readlines()
f.close()
models = []
for i, vals in enumerate(param_values):

        models.append('lc16.newmg.chabrier_wave1_optimization'+str(i)+'_expanded_range')
        
models = ' '.join(models)

contents[170] = 'foreach model ( '+models+' )\n'
contents[63]  = '    set nvol = 1-'+str(subvols)+'\n'
contents[176]  = '        set script = '+runscript+'\n'

f = open(newNameqsub, 'w')
contents = ''.join(contents)
f.write(contents)
f.close()
