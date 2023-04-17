# Simple script to compare two dataframes to see if they contain the same parameter values
import pandas as pd

param_file1_df = pd.read_csv("test_parameters_extended_v2.csv")
param_file2_df = pd.read_csv("test_parameters_extended_v3.csv")
param_file_df = param_file1_df.append(param_file2_df, ignore_index=True)

param_file3_df = pd.read_csv("test_parameters_extended_1000v1.csv")

# Find the index where columns match. Can do this for a single or multiple dataframe column.
# Aim is to find no matching parameter values
mask = (param_file_df.isin(param_file3_df)).all(axis=1)
print(param_file_df[mask])

print(len(param_file3_df))