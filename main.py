# positiveIncrease is the column that contains the count of new cases for the day

import os
import sys
import datetime
import numpy as np
import pandas as pd
from benford import apply_benford
from covid import df

states = [
    'AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE',
    'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY',
    'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT',
    'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK',
    'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA',
    'VI', 'VT', 'WA', 'WI', 'WV', 'WY']

# only keep recs with good data quality
# df = df[(df.dataQualityGrade == 'A+') | 
#         (df.dataQualityGrade == 'A') | 
#         (df.dataQualityGrade == 'B')]

for s in states:
    p = list(df[df.state == s].positiveIncrease)
    n = sum([1 if i < 0 else 0 for i in p])
    z = sum([1 if i == 0 else 0 for i in p])
    p = [n for n in p if n > 0]
    print('{}-{} (removed {} zeros, {} negatives):'.format(s, len(p), z, n))
    if len(p) == 0:
        print('no data')
        continue
    fs = apply_benford(p)
    for i, f in enumerate(fs):
        print('frequency for {}: {:>5.1%}'.format((i + 1), f))




