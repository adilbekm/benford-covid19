# World script (quick version):
# 
# - read pre-processed source data: world.csv
# - apply Benford's Law to select locations
# - output plots for select locations
# 
# The data source is csv files from Johns Hopkins University:
# https://github.com/CSSEGISandData/COVID-19


import numpy as np
import pandas as pd
import math
from benford import plot_benford


# locations (country, province) to apply Benford's Law 
locs_benford = [
    ('South Korea', None),
    ('United Kingdom', 'England'),
    ('China', 'Beijing'),
    ('China', 'Hunan'),
    ('China', 'Shanghai'),
    ('Canada', 'British Columbia'),
    ('Denmark', None),
    ('France', None),
    ('Germany', None),
    ('Germany', 'Berlin'),
    ('India', 'Punjab'),
    ('Israel', None),
    ('Italy', None),
    ('Japan', None),
    ('Sweden', 'Stockholm'),
    ('Sweden', None),
    ('Turkey', None),
    ('United Arab Emirates'),
    ('Zimbabwe', None),
    ('Libya', None),
    ('India', 'Delhi'),
    ('Lithuania', None),
    ('Latvia', None),
    ('Burma', None),
    ('Poland', None),
    ('Romania', None),
    ('Lithuania', None),
    ('Kyrgyzstan', None),
    ('Kazakhstan', None),
    ('Uzbekistan', None),
    ('Tajikistan', None),
    ('Russia', 'Moscow'),
    ('Russia', 'Saint Petersburg'),
    ('Russia', 'Khabarovsk Krai')]


def plot_benford_world(df, locs):
    '''Given dataframe, df, and list of (country, province) tuples, locs,
    applies Benford's Law to each location, and creates .png file for each.
    '''
    for loc_tuple in locs:
        
        loc = loc_tuple[0]
        pro = loc_tuple[1]
        
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
    
        loc = loc.replace(' ', '_')
        if pro:
            pro = pro.replace(' ', '_')
            loc = loc + '_' + pro
        title = 'Covid-19 Daily Cases: {}\n{} numbers from {} to {}'
        title = title.format(loc, len(p), min_date, max_date)
        fname ='{}.png'.format(loc.lower())
        path = 'world_output'
    
        plot_benford(p, title, fname, path)


if __name__ == '__main__':
    print('[BEG] begin processing')
    src_fn = 'world.csv'
    src = open(src_fn, encoding='utf8')
    df = pd.read_csv(src, sep='|')
    print('[OK ] source data loaded to dataframe')
    plot_benford_world(df, locs_benford)
    print('[END] world output is ready')

