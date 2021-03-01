# World script:
# 
# - read input data from world_data/
# - combine related country names
# - remove US data
# - compute increases, i.e. daily positive cases
# - apply Benford's Law to all locations
# - output plots for all locations: world_output/[location].png
# - output location ranks by error: world_rank.csv
# - save dataframe: extra/world.csv
# - save list of countries: extra/locations.csv
# 
# The data source is csv files from Johns Hopkins University:
# https://github.com/CSSEGISandData/COVID-19


import os
import math
import numpy as np
import pandas as pd
from datetime import date
from benford import benford_error, plot_benford_world


print('[BEG] begin processing')


# -----------------------------------------------------------------
# initial setup

# file for saving processed dataframe
dst_fn = 'extra/world.csv'
try: os.remove(dst_fn)
except OSError: pass
dst = open(dst_fn, 'a', encoding='utf8')

# file for saving location names
locf_fn = 'extra/world_locations.csv'
try: os.remove(locf_fn)
except OSError: pass
locf = open(locf_fn, 'a', encoding='utf8')
locf.write('Location,Province\n')

# file for saving location ranks by error
rfn = 'world_rank.csv'
try: os.remove(rfn)
except OSError: pass
rf = open(rfn, 'a', encoding='utf8')
rf.write('Location,Province,Numbers,Error,Rank\n')

# get list of source files (csv files)
p = os.getcwd()
p += '/world_data'
fns = os.listdir(p) # file names in world_data/


print('[OK ] {} files found in {}/'.format(len(fns), p[-10:]))


def safe_string(s):
    '''Given string s, returns simplified and cleaned version
    by removing any characters other than space and latin letters.
    '''
    s = s.strip()
    s = s.replace('-', ' ')
    slist = []
    cs = 0 # consequtive space
    for c in s:
        if ord(c) == 32: # space
            cs += 1
            if cs < 2:
                slist.append(c)
        elif ((ord(c) > 64 and ord(c) < 91) or  # capital letters
              (ord(c) > 96 and ord(c) < 123)):  # small letters
            cs = 0
            slist.append(c)
        else:
            cs = 0
    s = ''.join(slist)
    return s


# def safe_string(s):
#     '''Given string s, returns cleaned and simplified version.
#     '''
#     s = s.strip()
#     s = s.replace(' ', '_')
#     s = s.replace('-', '_')
#     slist = []
#     for c in s:
#         if (ord(c) == 95                        # _ underscore
#             or (ord(c) > 64 and ord(c) < 91)    # capital letters
#             or (ord(c) > 96 and ord(c) < 123)): # small letters
#             slist.append(c)
#     s = ''.join(slist)
#     return s


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

# expected column structure in csv files:
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


# -----------------------------------------------------------------
# read csv files to dictionary

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
    
    # clean up location names
    locs = [safe_string(str(l)) for l in locs]
    prov = [safe_string(str(p)) for p in prov]

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


# -----------------------------------------------------------------
# combine related country names: dups[n][0] => dups[n][1]

dups = [
    ('Bahamas The', 'Bahamas'),
    ('The Bahamas', 'Bahamas'),
    ('UK', 'United Kingdom'),
    ('Gambia The', 'Gambia'),
    ('The Gambia', 'Gambia'),
    ('Iran Islamic Republic of', 'Iran'),
    ('Korea South', 'South Korea'),
    ('Republic of Korea', 'South Korea'),
    ('Republic of Moldova', 'Moldova'),
    ('Republic of Ireland', 'Ireland'),
    ('Mainland China', 'China'),
    ('Russian Federation', 'Russia'),
    ('Viet Nam', 'Vietnam'),
    ('occupied Palestinian territory', 'Palestine')]

for dup in dups:
    loc = dst_dict['location']
    dst_dict['location'] = [dup[1] if c == dup[0] else c for c in loc]


# -----------------------------------------------------------------
# import to dataframe

# set to zero so that dictionary can be imported to dataframe
dst_dict['cases_inc'].extend([0 for i in range(len(dst_dict['cases']))])
dst_dict['deaths_inc'].extend([0 for i in range(len(dst_dict['deaths']))])

df = pd.DataFrame(dst_dict)
print('[OK ] dataframe created with len={:,}'.format(len(df)))

df = df[df.location != 'US']
print('[OK ] usa data removed, remaining len={:,}'.format(len(df)))

df = df.sort_values(by=['location', 'province', 'file_date'], ignore_index=True)


# -----------------------------------------------------------------
# compute increases (daily numbers), and save location info

prev_loc = None
prev_cases = prev_deaths = 0
loc_prov = []

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
    else:
        # save location to list and file
        loc_prov.append((location, province))
        locf.write('{},{}\n'.format(location, province))
    
    prev_loc = loc
    prev_cases = cases
    prev_deaths = deaths

print('[OK ] daily numbers computed')
print('[OK ] location names saved in file {}'.format(locf_fn))


# -----------------------------------------------------------------
# save dataframe to file

df.to_csv(dst, index=False, sep='|')
dst.close()
print('[OK ] dataframe saved in file {}'.format(dst_fn))


# -----------------------------------------------------------------
# compute location ranks by error size

err_list = []
err_loc_list = []

for lp in loc_prov:
    l = lp[0] # location
    p = lp[1] # province

    df1 = df[(df.location == l) & (df.province == p)]
    
    n = list(df1.cases_inc)
    n = [num for num in n if num > 0]
    n_len = len(n)

    if n_len == 0:
        continue

    err = benford_error(n)
    err_list.append(err)
    err_loc_list.append([l, p, n_len, err])

err_list.sort()

for i in range(len(err_loc_list)):
    e = err_loc_list[i][3]
    e_index = err_list.index(e)
    rank = e_index + 1
    err_loc_list[i].append(rank)

err_loc_list.sort(key=lambda elr: elr[4])

# write to file
for el in err_loc_list:
    el = [str(e) for e in el]
    el = ','.join(el)
    rf.write(el + '\n')

print('[OK ] ranks computed and saved in file {}'.format(rfn))


# -----------------------------------------------------------------
# create benford plots for all locations, and save in png files
# use column 'cases_inc', i.e. daily positive cases

print('[INF] creating plots...')

plot_benford_world(df, loc_prov)


print('[END] world output is ready')

