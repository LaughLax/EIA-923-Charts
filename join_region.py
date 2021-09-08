import pandas as pd
import numpy as np

files = [r'raw\emissions_region2013.xlsx',
         r'raw\emissions_region2014.xlsx',
         r'raw\emissions_region2015.xlsx',
         r'raw\emissions_region2016.xlsx',
         r'raw\emissions_region2017.xlsx',
         r'raw\emissions_region2018.xlsx',
         r'raw\emissions_region2019.xlsx',
         ]

dfs = []
for filename in files:
    print(f'Reading {filename}')
    dfs.append(pd.read_excel(filename,
                             header=1,
                             index_col=[0],
                             nrows=62,
                             ))
    dfs[-1] = dfs[-1].rename(columns=lambda s: s.replace('\n',' ').strip())
    
print('Combining data...')
df_master = dfs[0]
for i in range(1, len(dfs)):
    df_master = df_master.append(dfs[i])

print('Writing to file...')
df_master.to_pickle(r'modified\Emission_Regions.pkl')
print('Done!')
