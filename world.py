# Script for reading data from .csv files in ./covid-world directory
# and combining select columns into one file: covid-world.csv
# The combined file will exclude US data.
# The csv files are from: https://github.com/CSSEGISandData/COVID-19

import os
from datetime import date
import numpy as np
import pandas as pd

# dest file
dst_fn = 'covid-world.csv'
try: os.remove(dst_fn)
except OSError: pass
dst = open(dst_fn, 'a', encoding='utf8')

# get list of source files
p = os.getcwd()
p += '/covid-world'
fns = os.listdir(p) # file names in dir ./covid-world

print('[OK ] found {} files in dir {}'.format(len(fns), p))

def date_parse(ds):
    '''Parses string ds that represents a date and time,
    and returns the date object. Works with the following
    types of inputs:
    3/15/20 22:52
    3/15/2020 22:52
    2020-03-15 22:52:08
    2020-03-15T22:52:08
    '''
    d = ds.split()
    if len(d) != 2:
        d = ds.split('T')
    d = d[0]
    if '/' in d: # in format 3/15/20 or 3/15/2020
        d = d.split('/')
        mm = int(d[0])
        dd = int(d[1])
        if len(d[2]) == 2:
            d[2] = '20' + d[2]
        yy = int(d[2])
        return date(year=yy, month=mm, day=dd)
    return date.fromisoformat(d)

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

# dest dict
dst_dict = {
    'location':   [], # df.Country_Region
    'province':   [], # df.Province_State
    'last_upd':   [], # df.Last_Update
    'cases':      [], # df.Confirmed
    'cases_inc':  [], # [computed, daily increase]
    'deaths':     [], # df.Deaths
    'deaths_inc': [], # [computed, daily increase]
    'src_file':   []} # [source file name]

for fn in fns:
    pfn = p + '/' + fn
    f = open(pfn, 'r', encoding='utf8')
    df = pd.read_csv(f)
    col = list(df.columns)
    if 'Province/State' in col:
        try:
            assert 'Province/State' in col
            assert 'Country/Region' in col
            assert 'Last Update' in col
            assert 'Confirmed' in col
            assert 'Deaths' in col
        except AssertionError:
            print('[ERR] skipping file {}, unexpected columns'.format(fn))
            continue
        prov = list(df['Province/State'])
        locs = list(df['Country/Region'])
        dats = list(df['Last Update'])
    else:
        try:
            assert 'Province_State' in col
            assert 'Country_Region' in col
            assert 'Last_Update' in col
            assert 'Confirmed' in col
            assert 'Deaths' in col
        except AssertionError:
            print('[ERR] skipping file {}, unexpected columns'.format(fn))
            continue
        prov = list(df.Province_State)
        locs = list(df.Country_Region)
        dats = list(df.Last_Update)
    try:
        dats = [date_parse(d) for d in dats]
    except:
        print('[ERR] file {} has problem with dates'.format(fn))
        continue
    locs = [s.strip() for s in locs]
    cses = list(df.Confirmed)
    dths = list(df.Deaths)
    fnms = [fn for i in range(len(df))]
    dst_dict['location'].extend(locs)
    dst_dict['province'].extend(prov)
    dst_dict['last_upd'].extend(dats)
    dst_dict['cases'].extend(cses)
    dst_dict['deaths'].extend(dths)
    dst_dict['src_file'].extend(fnms)

dst_dict['cases_inc'].extend([0 for i in range(len(dst_dict['cases']))])
dst_dict['deaths_inc'].extend([0 for i in range(len(dst_dict['deaths']))])
print('[OK ] dict created from files')

df = pd.DataFrame(dst_dict)
print('[OK ] dataframe created of len {}'.format(len(df)))

df = df[df.location != 'US']
print('[INF] removed US records')

df = df.sort_values(by=['location', 'province', 'last_upd'])
print('[OK ] dataframe sorted by location, province, last_upd')

df.to_csv(dst, index=False, sep='|')
print('[OK ] dataframe saved in file {}'.format(dst_fn))

