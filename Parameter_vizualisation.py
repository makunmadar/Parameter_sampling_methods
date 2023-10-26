import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 10
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)

column_names = [r'$\alpha_{ret}$', r'$V_{SN,disk}$', r'$V_{SN,burst}$', r'$\gamma_{SN}$', r'$\alpha_{cool}$',
                r'$\nu_{SF}$', r'$F_{stab}$', r'$f_{ellip}$', r'$f_{burst}$', r'$f_{SMBH}$',  r'$\tau_{* burst, min}$']
raw_dataset = pd.read_csv('updated_parameters_3000v4.csv', names=column_names, sep=',', skiprows=1)
dataset = raw_dataset.copy()

# sns.pairplot(dataset[['alpha_reheat', 'vhotdisk', 'vhotburst', 'alphahot', 'alpha_cool', 'nu_sf', 'Fstab', 'fellip',
#                 'fburst', 'fSMBH',  'tau_burst']], diag_kind='hist', plot_kws={"s": 2})
sns.pairplot(dataset[[r'$\alpha_{ret}$', r'$V_{SN,disk}$', r'$V_{SN,burst}$',]], diag_kind='hist',
             plot_kws={"s": 2}, diag_kws={'bins': 20})
plt.savefig('Pairplot_parameters.png')
plt.show()
