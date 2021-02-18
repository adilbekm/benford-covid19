# USA script:
# read raw data, apply Benford's Law, and output plots by state

import os
import sys
import datetime
import numpy as np
import pandas as pd
from benford import apply_benford, plot_benford


# Step 1. Read USA covid-19 data to pandas dataframe.
# The data source is Covid Tracking Project: https://covidtracking.com

print('Please wait...')

src_name = 'usa_data/all-states-history.csv'
src = open(src_name, 'r', encoding='utf8')
df = pd.read_csv(src)

# df = df.astype({
    # 'date': 'datetime64[ns]',
    # 'state': 'string',
    # 'dataQualityGrade': 'string'
    # 'death': 'int64',
    # 'deathConfirmed': 'int64',
    # 'deathIncrease': 'int64',
    # 'deathProbable': 'int64',
    # 'hospitalized': 'int64',
    # 'hospitalizedCumulative': 'int64',
    # 'hospitalizedCurrently': 'int64',
    # 'hospitalizedIncrease': 'int64',
    # 'inIcuCumulative': 'int64',
    # 'inIcuCurrently': 'int64',
    # 'negative': 'int64',
    # 'negativeIncrease': 'int64',
    # 'negativeTestsAntibody': 'int64',
    # 'negativeTestsPeopleAntibody': 'int64',
    # 'negativeTestsViral': 'int64',
    # 'onVentilatorCumulative': 'int64',
    # 'onVentilatorCurrently': 'int64',
    # 'positive': 'int64',
    # 'positiveCasesViral': 'int64',
    # 'positiveIncrease': 'int64',
    # 'positiveScore': 'int64',
    # 'positiveTestsAntibody': 'int64',
    # 'positiveTestsAntigen': 'int64',
    # 'positiveTestsPeopleAntibody': 'int64',
    # 'positiveTestsPeopleAntigen': 'int64',
    # 'positiveTestsViral': 'int64',
    # 'recovered': 'int64',
    # 'totalTestEncountersViral': 'int64',
    # 'totalTestEncountersViralIncrease': 'int64',
    # 'totalTestResults': 'int64',
    # 'totalTestResultsIncrease': 'int64',
    # 'totalTestsAntibody': 'int64',
    # 'totalTestsAntigen': 'int64',
    # 'totalTestsPeopleAntibody': 'int64',
    # 'totalTestsPeopleAntigen': 'int64',
    # 'totalTestsPeopleViral': 'int64',
    # 'totalTestsPeopleViralIncrease': 'int64',
    # 'totalTestsViral': 'int64',
    # 'totalTestsViralIncrease': 'int64'})


# Step 2. Apply Benford's Law by state, and save resulting plots to PNG files.
# The column to use for analysys is "positiveIncrease" i.e. the count of daily new cases.

states = [
    'AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE',
    'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY',
    'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT',
    'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK',
    'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA',
    'VI', 'VT', 'WA', 'WI', 'WV', 'WY']

for s in states:
    p = list(df[df.state == s].positiveIncrease)
    n = sum([1 if i < 0 else 0 for i in p])
    z = sum([1 if i == 0 else 0 for i in p])
    p = [n for n in p if n > 0]
    
    min_date = df[df.state == s].date.min()
    max_date = df[df.state == s].date.max()
    
    # print('{}-{} (removed {} zeros, {} negatives):'.format(s, len(p), z, n))
    
    if len(p) == 0:
        # print('no data')
        continue
    
    fs = apply_benford(p)
    
    # for i, f in enumerate(fs):
    #     print('frequency for {}: {:>5.1%}'.format((i + 1), f))

    title = 'Covid-19 Daily Cases: {}, USA\n{} numbers from {} to {}'
    title = title.format(s, len(p), min_date, max_date)
    fname ='usa_{}.png'.format(s.lower())
    path = 'usa_output'
    plot_benford(p, title, fname, path)

print('USA output is ready')

