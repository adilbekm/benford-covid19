# module for reading data from .csv file in ./covid-world directory
# and combining select columns into one file: covid-world.csv

import os
import numpy as np
import pandas as pd

# dest file
dst_fn = 'covid-world.csv'
try: os.remove(dst_fn)
except OSError: pass
dst = open(dst_fn, 'a', encoding='utf8')

# dest dict
dst_d = {}

# get list of source files
p = os.getcwd()
p += '/covid-world'
fns = os.listdir(p) # file names in dir ./covid-world

print('[OK ] found {} files in dir {}'.format(len(fns), p))

# expected column structure
col_exp = [
    'FIPS',
    'Admin2', 
    'Province_State', 
    'Country_Region', 
    'Last_Update', 
    'Lat', 
    'Long_', 
    'Confirmed', 
    'Deaths', 
    'Recovered', 
    'Active', 
    'Combined_Key', 
    'Incidence_Rate', 
    'Case-Fatality_Ratio']

for fn in fns:
    print('[OK ] start work on file {}'.format(fn))
    pfn = p + '/' + fn
    f = open(pfn, 'r', encoding='utf8')
    df = pd.read_csv(f)
    print('[OK ] file loaded into df')
    col = list(df.columns)
    if col != col_exp:
        raise 'Unexpected column structure in file {}'.format(fn)
    print(df.info())
    break



