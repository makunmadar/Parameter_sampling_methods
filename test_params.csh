#!/usr/bin/env tcsh

set logpath = /cosma5/data/durham/dc-mada1/LOGS/em_lines_test/
set Nbody_sim = L800
set iz_list = (214)
set nvol = 1-1

echo 'Redshifts: ' $iz_list
echo 'Volumes: ' $nvol

foreach line ( "`tail -n +2 test_parameters.csv`")

    # List out the individual parameters of each row.
    set alpha_reheat_new = `echo $line | cut -d "," -f 1`
    set vhotdisk_new = `echo $line | cut -d "," -f 2`
    set vhotburst_new = `echo $line | cut -d "," -f 3`
    set alphahot_new = `echo $line | cut -d "," -f 4`
    set alpha_cool_new = `echo $line | cut -d "," -f 5`
    set nu_sf_new = `echo $line | cut -d "," -f 6`

    # Able to do all the work from here one row at a time
    foreach iz ($iz_list)

        set script = run_galform_mod.csh
        set jobname = parameter_searching_test_outputs
        set logname = ${logpath}/${Nbody_sim}/Param_search/testing_outputs.%A.%a.log
        \mkdir -p ${logname:h}

        # Construct a batch script and submit it to SLURM as an array job -
        # the script consists of the Slurm header below followed by the
        # contents of ${script}.
        cat << EOF - ${script} | sbatch --array=${nvol}

#!/bin/tcsh -ef
#
#SBATCH --ntasks 1
#SBATCH -J ${jobname}
#SBATCH -o ${logname}
#SBATCH -p cordelia
#SBATCH -A durham
#SBATCH -t 72:00:00
#

# Set parameters
set model            = ${model}
set Nbody_sim        = ${Nbody_sim}
set iz               = ${iz}
set alpha_reheat_new = ${alpha_reheat_new}
set vhotdisk_new     = ${vhotdisk_new}
set vhotburst_new    = ${vhotburst_new}
set alphahot_new     = ${alphahot_new
set alpha_cool_new   = ${alpha_cool_new}
set nu_sf_new        = ${nu_sf_new}
@ ivol        = \${SLURM_ARRAY_TASK_ID} - 1

# Galform run script follows
EOF

    end
end


