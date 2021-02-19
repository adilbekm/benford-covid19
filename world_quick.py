# World script (quick version):
# 
#   read preprocessed source data: world.csv
#   combine related country names
#   load to dataframe
#   remove US data
#   compute increases, i.e. daily numbers
#   save dataframe to world.csv
#   apply Benford's Law to select locations
#   output plots for select locations
# 
# The data source is csv files from:
# https://github.com/CSSEGISandData/COVID-19
# (Johns Hopkins University)


# import os
# from datetime import date
import numpy as np
import pandas as pd
import math
from benford import plot_benford


# locations (country, province) for Benford's Law output
blocs = [
    ('South Korea', None),
    ('United Kingdom', 'England'),
    ('Libya', None),
    ('India', 'Delhi'),
    ('Lithuania', None),
    ('Burma', None),
    ('Sweden', None),
    ('Poland', None),
    ('Romania', None),
    ('Lithuania', None),
    ('Kyrgyzstan', None),
    ('Kazakhstan', None),
    ('Uzbekistan', None),
    ('Tajikistan', None),
    ('Russia', 'Moscow')]


print('[BEG] begin processing')

# source data
src_fn = 'world.csv'
src = open(src_fn, encoding='utf8')
df = pd.read_csv(src, sep='|')
print('[OK ] source data loaded to dataframe')

# apply benford to selected locations
for bloc in blocs:
    
    loc = bloc[0]
    pro = bloc[1]
    
    if pro is None:
        df1 = df[(df.location == loc) & (df.province.isna())]
    else:
        df1 = df[(df.location == loc) & (df.province == pro)]
   
    p = list(df1.cases_inc)
    p = [n for n in p if n > 0]

    if len(p) == 0:
        continue

    min_date = df1.file_date.min()
    max_date = df1.file_date.max()

    if pro:
        loc = loc + '_' + pro
    title = 'Covid-19 Daily Cases: {}\n{} numbers from {} to {}'
    title = title.format(loc, len(p), min_date, max_date)
    fname ='{}.png'.format(loc.lower())
    path = 'world_output'

    plot_benford(p, title, fname, path)

print('[END] world output created')

