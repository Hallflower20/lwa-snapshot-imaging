import os
import sys
import subprocess

input = sys.argv
input.pop(0)
#print(input)
file_name, data_dir, image_output, antenna = input
msfile_name = file_name.split("/")[-1].split(".")
msfile_prefix = msfile_name[0]
if(len(msfile_name) == 1 or msfile_name[1] != "ms"):
    raise ValueError("Input file must be a ms file, " + str(file_name) + " is not a ms file!")
if(not(os.path.exists(file_name))):
    raise ValueError("The MS File at " + str(file_name) + " does not exist")

#scratch_space_new = os.path.join(scratch_space, msfile_prefix)
#if(not(os.path.exists(scratch_space_new))):
#    os.mkdir(scratch_space_new)

image_output_new = os.path.join(image_output, msfile_prefix)
if(not(os.path.exists(image_output_new))):
    os.mkdir(image_output_new)

c6 = 'eval "$(conda shell.bash hook)"'
c7 = "conda activate deployment"
c8 = "casa"
c9 = "antenna = '{}'".format(antenna)
c10 = "flagdata('{}', antenna = antenna, datacolumn = 'all')".format(file_name)
c11 = "clearcal('{}', addmodel=True)".format(file_name)
c12 = "ft('{}', complist = '{}.cl', usescratch=True)".format(file_name, msfile_prefix)
c13 = "bandpass('{}', '{}.bcal', uvrange='>15lambda',fillgaps=1)".format(file_name, msfile_prefix)
c14 = "applycal('{}', gaintable=['{}.bcal'], flagbackup=False)".format(file_name, msfile_prefix)
c15 = "flagdata('{}', mode = 'rflag', antenna = antenna, datacolumn = 'CORRECTED')".format(file_name)
c16 = "exit"
c18 = "/opt/bin/wsclean -pol I -multiscale -multiscale-scale-bias 0.9 -size 4096 4096 -scale 0.03 -niter 10000 -mgain 0.85 -weight briggs 0 -name {} {}".format(os.path.join(image_output_new ,msfile_prefix), file_name)

cl_file = os.path.join(data_dir, msfile_prefix + ".cl")
if(os.path.exists(cl_file)):
    subprocess.run(["rm", "-r", cl_file])
subprocess.run(["sh", "/home/xhall/GitHub/lwa-snapshot-imaging/cl_maker.sh", file_name])

commands = [c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16]

print(subprocess.call(commands, shell = True))

subprocess.call(["sh", "/home/xhall/GitHub/lwa-snapshot-imaging/im_maker.sh", os.path.join(image_output_new ,msfile_prefix), file_name])
