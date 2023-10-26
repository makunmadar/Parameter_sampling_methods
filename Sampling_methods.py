from scipy.stats import qmc
import pandas as pd

# Define the upper and lower bounds for each parameter
parabounds = {'alpha_reheat': [0.2, 3.0],
              'vhotdisk': [10, 800],
              'vhotburst': [10, 800],
              'alphahot': [1.0, 4.0],
              'alpha_cool': [0.0, 4.0],
              'nu_sf': [0.1, 4.0],
              'Fstab': [0.5, 1.2],  # stabledisk
              'fellip': [0.2, 0.5],  # fellip
              'fburst': [0.01, 0.3],  # fburst
              'fSMBH': [0.001, 0.05],  # F_SMBH
              'tau_burst': [0.01, 0.2]  #tau_star_min_burst Lacey goes up to 0.1.
              }

seed = 42

df = pd.DataFrame(parabounds)
headers = df.columns

engine = qmc.LatinHypercube(d=11, seed=seed)  # d will equal the number of parameters
sample = engine.random(n=1000)  # n is the number of samples per parameter

bounds = df.values.tolist()

lhc = qmc.scale(sample, bounds[0], bounds[1])

parasamp = pd.DataFrame(lhc, columns=headers)
print(parasamp)

additional_samples = engine.random(n=2000)
# Remove the samples that were already in "parasamp"
additional_samples = additional_samples[len(parasamp):]

additional_samples = qmc.scale(additional_samples, bounds[0], bounds[1])

additional_df = pd.DataFrame(additional_samples, columns=parasamp.columns)
print(additional_df)

# Concatenate the additional samples to the existing DataFrame
new_parasamp = pd.concat([parasamp, additional_df], ignore_index=True)

# Even more 1000 runs
evenmore_samples = engine.random(n=3000)
# Remove the samples already in "new_parasamp"
evenmore_samples = evenmore_samples[len(new_parasamp):]

evenmore_samples = qmc.scale(evenmore_samples, bounds[0], bounds[1])

evenmore_df = pd.DataFrame(evenmore_samples, columns=parasamp.columns)
print(evenmore_df)

# Concatenate the additional samples to the existing DataFrame
evenmore_parasamp = pd.concat([new_parasamp, evenmore_df], ignore_index=True)

evenmore_parasamp.to_csv('updated_parameters_3000v4.csv', sep=',', index=False)
