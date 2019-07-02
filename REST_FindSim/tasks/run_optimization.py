import subprocess
import re
import zipfile
import os

from .utility import OptimizationResult, parse_output, decode_bytes
from .run_findSim import run_findSim


def run_optimization( tsv_zip, model_file , file_label, optimized_model, num_processes = 2, tolerance = 1e-4):
    t_result = OptimizationResult()

    # Validation of .tsv file and modle file
    fs = tsv_zip.split('.')
    if len(fs) < 2 or fs[-1] != 'zip' or len(tsv_zip) < 5:
        t_result.set_error('Invalid .tsv zip file type.')
    fs = []
    fs = model_file.split('.')
    if len(fs) < 2 or (fs[-1] != 'g' and fs[-1] != 'xml'):
        t_result.set_error('Invalid model file type.')

    if t_result.error:
        return t_result

    # Unzip .tsv files and save them into a directory
    f = zipfile.ZipFile(tsv_zip, 'r')
    for file in f.namelist():
        f.extract(file,'files/tsv/'+file_label)
    f.close()

    # Firstly, run findSim to generate parameters list for each .tsv file
    tsv_file_path = tsv_zip[0:len(tsv_zip)-4]

    # Record parameters in a dictionary
    param_list_d = {}

    for root, dirs, files in os.walk(tsv_file_path, topdown=False):
        # Check if there exists files
        if len(files) == 0:
            t_result.set_error("No .tsv file in directory")
            return t_result
        # For each .tsv file in the directory
        for file in files:
            # Run findSim to generate param list, use '-p'
            tmp_param_list_path = os.path.join(root,"tmp_param_list.txt")
            # Set param file : tmp_param_list_path
            # and set hp : True
            # Check if there exists wrong file type
            if file.split('.')[-1] != 'tsv':
                t_result.set_error("Wrong file type in directory: "+file)
                return t_result
            # Run FindSim
            tmp_file_path = os.path.join(root,file)
            run_findSim( tmp_file_path, model_file , "", tmp_param_list_path, True)
            # Fetch params and add them into dictionary
            try:
                tmp_param_list = open(tmp_param_list_path, 'r+')
                param = tmp_param_list.readline().strip()
                # For each param
                while param:
                    tmp_contents = param.split('   ')
                    assert(len(tmp_contents) == 2)
                    param = tmp_contents[0]+'.'+tmp_contents[1]
                    if param not in param_list_d:
                        param_list_d[param] = True
                    param = tmp_param_list.readline().strip()
            except OSError:
                t_result.set_error('Error when open param list(while running FindSim)')
                return t_result
            else:
                tmp_param_list.close()

    # Secondly, run optimization according to parameter list
    # Generate param list:
    param_list_commandline = ""
    for param in param_list_d.keys():
        param_list_commandline += param + ' '
    # Generate command line:
    command_Optimization = 'python third_party/FindSim/multi_param_minimization.py '\
                           + tsv_file_path\
                           + ' -n ' + str(num_processes)\
                           + ' -m ' + model_file\
                           + ' -f ' + optimized_model\
                           + ' -p ' + param_list_commandline\
                           + ' -t ' + str(tolerance)

    # Run Optimization via subprocess
    p = subprocess.Popen(command_Optimization,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output_info, error_info = p.communicate()
    p.wait()
    # Parse output
    t_result = parse_output(decode_bytes(output_info),decode_bytes(error_info),"Optimization")
    t_result.set_model(optimized_model)

    return t_result
