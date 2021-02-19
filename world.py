# World script:
# 
#   read source data in world_data/
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


import os
from datetime import date
import numpy as np
import pandas as pd
import math
from benford import plot_benford


print('[BEG] begin processing')

# dest file
dst_fn = 'world.csv'
try: os.remove(dst_fn)
except OSError: pass
dst = open(dst_fn, 'a', encoding='utf8')

# get list of source files
p = os.getcwd()
p += '/world_data'
fns = os.listdir(p) # file names in dir ./world_data

print('[OK ] found {} files in dir {}'.format(len(fns), p))


# locations (country, province) for Benford's Law output
blocs = [
    ('South Korea', None),
    ('Libya', None),
    ('India', 'Delhi'),
    ('Lithuania', None),
    ('Kazakhstan', None),
    ('Uzbekistan', None),
    ('Russia', 'Moscow')]


def date_parse(ds):
    '''Parses string, ds, that represents a date and time,
    and returns the date object. Works with the following
    types of inputs (examples):
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
#  'FIPS',
#  'Admin2', 
#  'Province_State', 
#  'Country_Region', 
#  'Last_Update', 
#  'Lat', 
#  'Long_', 
#  'Confirmed', 
#  'Deaths', 
#  'Recovered', 
#  'Active', 
#  'Combined_Key', 
#  'Incidence_Rate', 
#  'Case-Fatality_Ratio'


# dest dict
dst_dict = {
    'location':   [], # df.Country_Region
    'province':   [], # df.Province_State
    'last_upd':   [], # df.Last_Update
    'file_date':  [], # [date based on source file name]
    'cases':      [], # df.Confirmed
    'cases_inc':  [], # [computed, daily increase]
    'deaths':     [], # df.Deaths
    'deaths_inc': [], # [computed, daily increase]
    'src_file':   []} # [source file name]


for fn in fns: # for each csv file
    pfn = p + '/' + fn
    f = open(pfn, 'r', encoding='utf8')
    df = pd.read_csv(f)

    col = list(df.columns)
    # column names can have one of two literations, so check which one
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
    
    cses = list(df.Confirmed)
    dths = list(df.Deaths)
    
    locs = [s.strip() for s in locs]

    # parse file name (ex: '03-15-2020.csv') into date object
    fl = fn[0:10].split('-')
    fl = [int(s) for s in fl]
    fd = date(year=fl[2], month=fl[0], day=fl[1])
    
    fnds = [fd for i in range(len(df))]
    fnms = [fn for i in range(len(df))]

    dst_dict['location'].extend(locs)
    dst_dict['province'].extend(prov)
    dst_dict['last_upd'].extend(dats)
    dst_dict['file_date'].extend(fnds)
    dst_dict['cases'].extend(cses)
    dst_dict['deaths'].extend(dths)
    dst_dict['src_file'].extend(fnms)


print('[OK ] data imported to dictionary')


# combine related country names: dups[n][0] => dups[n][1]
dups = [
    ('Bahamas, The', 'Bahamas'),
    ('The Bahamas', 'Bahamas'),
    ('UK', 'United Kingdom'),
    ('Gambia, The', 'Gambia'),
    ('The Gambia', 'Gambia'),
    ('Iran (Islamic Republic of)', 'Iran'),
    ('Korea, South', 'South Korea'),
    ('Republic of Korea', 'South Korea'),
    ('Republic of Moldova', 'Moldova'),
    ('Republic of Ireland', 'Ireland'),
    ('Mainland China', 'China'),
    ('Russian Federation', 'Russia'),
    ('Taiwan*', 'Taiwan'),
    ('Viet Nam', 'Vietnam'),
    ('occupied Palestinian territory', 'Palestine')]

for dup in dups:
    loc = dst_dict['location']
    dst_dict['location'] = [dup[1] if c == dup[0] else c for c in loc]

# set to zero so that dictionary can be imported to dataframe
dst_dict['cases_inc'].extend([0 for i in range(len(dst_dict['cases']))])
dst_dict['deaths_inc'].extend([0 for i in range(len(dst_dict['deaths']))])

df = pd.DataFrame(dst_dict)
print('[OK ] dataframe created, len={:,}'.format(len(df)))

df = df[df.location != 'US']
print('[OK ] US data removed, len={:,}'.format(len(df)))

df = df.sort_values(by=['location', 'province', 'file_date'], ignore_index=True)


# compute increases, i.e. daily cases/deaths numbers
prev_loc = None
prev_cases = prev_deaths = 0
for i in range(len(df)):
    location = df.at[i, 'location']
    province = df.at[i, 'province']
    cases    = df.at[i, 'cases']
    deaths   = df.at[i, 'deaths']
    loc = str(location) + str(province)

    # some cases/deaths could be NaN; treat them as zero
    if math.isnan(cases):
        cases = 0
    if math.isnan(deaths):
        deaths = 0

    if loc == prev_loc:
        df.at[i, 'cases_inc'] = cases - prev_cases
        df.at[i, 'deaths_inc'] = deaths - prev_deaths
    
    prev_loc = loc
    prev_cases = cases
    prev_deaths = deaths


print('[OK ] daily numbers computed')


df.to_csv(dst, index=False, sep='|')
dst.close()
print('[OK ] dataframe saved in file {}'.format(dst_fn))


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

