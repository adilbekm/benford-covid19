# USA script:
# 
# - read input data from usa_data/
# - apply Benford's Law
# - output plots by state: usa_output/usa_[state_code].png
# - output state ranks by error: usa_rank.csv
# 
# The data source is Covid Tracking Project: https://covidtracking.com


import os
import sys
import datetime
import numpy as np
import pandas as pd
from benford import plot_benford, benford_error


# ------------------------------------------------------------------
# read USA covid-19 data to pandas dataframe

print('[BEG] begin processing')

src_name = 'usa_data/all-states-history.csv'
src = open(src_name, 'r', encoding='utf8')
df = pd.read_csv(src)

dst_name = 'extra/usa.csv'
try: os.remove(dst_name)
except OSError: pass
dst = open(dst_name, 'a', encoding='utf8')

rf_name = 'usa_rank.csv'
try: os.remove(rf_name)
except OSError: pass
rf = open(rf_name, 'a', encoding='utf8')
rf.write('Rank,State,StateName,Numbers,BenfordError,PlotName\n')

# df = df.astype({
#     'date': 'datetime64[ns]',
#     'state': 'string',
#     'dataQualityGrade': 'string'
#     'death': 'int64',
#     'deathConfirmed': 'int64',
#     'deathIncrease': 'int64',
#     'deathProbable': 'int64',
#     'hospitalized': 'int64',
#     'hospitalizedCumulative': 'int64',
#     'hospitalizedCurrently': 'int64',
#     'hospitalizedIncrease': 'int64',
#     'inIcuCumulative': 'int64',
#     'inIcuCurrently': 'int64',
#     'negative': 'int64',
#     'negativeIncrease': 'int64',
#     'negativeTestsAntibody': 'int64',
#     'negativeTestsPeopleAntibody': 'int64',
#     'negativeTestsViral': 'int64',
#     'onVentilatorCumulative': 'int64',
#     'onVentilatorCurrently': 'int64',
#     'positive': 'int64',
#     'positiveCasesViral': 'int64',
#     'positiveIncrease': 'int64',
#     'positiveScore': 'int64',
#     'positiveTestsAntibody': 'int64',
#     'positiveTestsAntigen': 'int64',
#     'positiveTestsPeopleAntibody': 'int64',
#     'positiveTestsPeopleAntigen': 'int64',
#     'positiveTestsViral': 'int64',
#     'recovered': 'int64',
#     'totalTestEncountersViral': 'int64',
#     'totalTestEncountersViralIncrease': 'int64',
#     'totalTestResults': 'int64',
#     'totalTestResultsIncrease': 'int64',
#     'totalTestsAntibody': 'int64',
#     'totalTestsAntigen': 'int64',
#     'totalTestsPeopleAntibody': 'int64',
#     'totalTestsPeopleAntigen': 'int64',
#     'totalTestsPeopleViral': 'int64',
#     'totalTestsPeopleViralIncrease': 'int64',
#     'totalTestsViral': 'int64',
#     'totalTestsViralIncrease': 'int64'})


# ------------------------------------------------------------------
# apply Benford's Law by state, and save resulting plots in png files
# use column 'positiveIncrease', i.e. daily positive cases

states = [
    'AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE',
    'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY',
    'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT',
    'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK',
    'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA',
    'VI', 'VT', 'WA', 'WI', 'WV', 'WY']

snames = ['Alaska', 'Alabama', 'Arkansas', 'American Samoa', 'Arizona',
    'California', 'Colorado', 'Connecticut', 'District of Columbia',
    'Delaware', 'Florida', 'Georgia', 'Guam', 'Hawaii', 'Iowa', 'Idaho',
    'Illinois', 'Indiana', 'Kansas', 'Kentucky', 'Louisiana',
    'Massachusetts', 'Maryland', 'Maine', 'Michigan', 'Minnesota',
    'Missouri', 'Northern Mariana Islands', 'Mississippi', 'Montana',
    'North Carolina', 'North Dakota', 'Nebraska', 'New Hampshire',
    'New Jersey', 'New Mexico', 'Nevada', 'New York', 'Ohio', 'Oklahoma',
    'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island',
    'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',
    'Virginia', 'U.S. Virgin Islands', 'Vermont', 'Washington',
    'Wisconsin', 'West Virginia', 'Wyoming']

err_list = []
err_state_list = []

for s in states:

    s_index = states.index(s)
    sname = snames[s_index]
    
    df1 = df[df.state == s]
    
    p = list(df1.positiveIncrease)
    n = sum([1 if i < 0 else 0 for i in p])
    z = sum([1 if i == 0 else 0 for i in p])
    p = [n for n in p if n > 0]
    p_len = len(p)
    
    if len(p) == 0:
        continue
    
    min_date = df1.date.min()
    max_date = df1.date.max()
    
    # print('{}-{} (removed {} zeros, {} negatives):'.format(s, len(p), z, n))
    # fs = apply_benford(p)
    # for i, f in enumerate(fs):
    #     print('frequency for {}: {:>5.1%}'.format((i + 1), f))

    title = 'Covid-19 Daily Cases: USA_{}\n{} numbers from {} to {}'
    title = title.format(s, len(p), min_date, max_date)
    fname ='usa_{}.png'.format(s.lower())
    path = 'usa_output'
    
    plot_benford(p, title, fname, path)

    err = benford_error(p)
    err_list.append(err)
    err_state_list.append([s, sname, p_len, err, fname])


# ------------------------------------------------------------------
# save dataframe

df = df.loc[:, ['date', 'state', 'death', 'deathIncrease', 'positive', 
    'positiveIncrease']]

df.sort_values(by=['state', 'date'], ignore_index=True, inplace=True)

df.rename(columns={'death':'deaths', 'deathIncrease':'deaths_inc', 
    'positive':'cases', 'positiveIncrease':'cases_inc'}, inplace=True)

def get_state_name(code):
    i = states.index(code)
    return snames[i]

df['state_name'] = df.state.apply(get_state_name)

df = df[['date', 'state', 'state_name', 'deaths', 'deaths_inc',
    'cases', 'cases_inc']]

df.to_csv(dst, index=False, sep='|')
dst.close()

print('[OK ] dataframe saved in file {}'.format(dst_name))


# ------------------------------------------------------------------
# compute state ranks by error size

err_list.sort()

for i in range(len(err_state_list)):
    e = err_state_list[i][3]
    e_index = err_list.index(e)
    rank = e_index + 1
    err_state_list[i].insert(0, rank)

# sort by rank
err_state_list.sort(key=lambda esr: esr[0])

# write to file
for es in err_state_list:
    es = [str(e) for e in es]
    es[4] = es[4][0:7] # truncate error to shorter decimal
    es = ','.join(es)
    rf.write(es + '\n')

print('[OK ] ranks saved in file {}'.format(rf_name))


print('[END] usa output is ready')

