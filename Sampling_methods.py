from scipy.stats import qmc
import pandas as pd

# Define the upper and lower bounds for each parameter
parabounds = {'alpha_reheat': [0.3, 3.0],
              'vhotdisk': [100, 550],
              'vhotburst': [100, 550],
              'alphahot': [1.5, 3.5],
              'alpha_cool': [0.0, 2.0],
              'nu_sf': [0.2, 1.7]
              }

seed = 1

df = pd.DataFrame(parabounds)
headers = df.columns

engine = qmc.LatinHypercube(d=6, seed=seed)  # d will equal the number of parameters
sample = engine.random(n=1000) # n is the number of samples per parameter

bounds = df.values.tolist()

lhc = qmc.scale(sample, bounds[0], bounds[1])

parasamp = pd.DataFrame(lhc, columns=headers)
print(parasamp)

# Update the parameters dataframe to include the redshifts and subvolumes for each parameter set.

parasamp.to_csv('test_parameters_1000v1.csv', sep=',', index=False)