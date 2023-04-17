import pandas as pd
from shutil import copyfile
import re

params = pd.read_csv("test_parameters.csv").round(2)
print(params)
param_names = params.columns

basefile = "Makun_L800_params_test.input.ref"

for index, row in params.iterrows():
    for name in param_names:
        print('Name: ', name, 'values: ', row[name])


# for i, par_name in enumerate(params):
#     with open(basefile, 'r') as file:
#         lines = file.readlines()
#         for line in lines:
#             if line.startswith(par_name):
#                 print(par_name, 'string exists in file')
#                 print('line: ', line)
#                 print(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", line))
