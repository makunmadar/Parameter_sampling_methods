import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

column_names = ['alpha_reheat', 'vhotdisk', 'vhotburst', 'alphahot', 'alpha_cool', 'nu_sf', 'Fstab', 'fellip',
                'fburst', 'fSMBH',  'tau_burst']
raw_dataset = pd.read_csv('updated_parameters_3000v4.csv', names=column_names, sep=',', skiprows=1)
dataset = raw_dataset.copy()

sns.pairplot(dataset[['alpha_reheat', 'vhotdisk', 'vhotburst', 'alphahot', 'alpha_cool', 'nu_sf', 'Fstab', 'fellip',
                'fburst', 'fSMBH',  'tau_burst']], diag_kind='hist', plot_kws={"s": 2})
plt.show()
