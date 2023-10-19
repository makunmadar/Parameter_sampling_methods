import pandas as pd

df = pd.read_csv('updated_parameters_3000v4.csv')
columns = df.columns.tolist()
extra_columns = ['redshift', 'subvolume', 'modelno']
columns.extend(extra_columns)

iz_list = [271, 194, 182, 169, 152, 142]
nvol_list = [1, 2, 3, 4, 5]

data = []
model_num = 0

for i in range(len(df)):
    model_num += 1
    for j in range(len(iz_list)):
        for k in range(len(nvol_list)):

            row = df.iloc[i].tolist()
            row.append(iz_list[j])
            row.append(nvol_list[k])
            row.append(model_num)
            data.append(row)

df_new = pd.DataFrame(columns=columns, data=data)
print(df_new)

df_new.to_csv('updated_parameters_extended_3000v4.csv', sep=',', index=False)
