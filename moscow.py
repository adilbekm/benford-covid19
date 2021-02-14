import os
import numpy as np
import pandas as pd
from datetime import date, timedelta

src_name = 'moscow.csv'
src = open(src_name, 'r', encoding='utf8')

dst_name = 'moscow_calc.csv'
try: os.remove(dst_name)
except OSError: pass
dst = open(dst_name, 'a', encoding='utf8')

i = 0
moscow_daily = []

for r in src:
    i += 1
    if i == 1: # this is header
        dst.write(r)
        dt_pr = None
    else:
        r = r.split('|')
        locs  = r[0]
        prov  = r[1]
        dt    = r[2]
        cases = r[3]
        death = r[5]

        dt = date.fromisoformat(dt)
        cases = int(float(cases))
        death = int(float(death))

        if dt_pr is None:
            cases_inc = 0
            death_inc = 0
        else:
            dt_delta = dt - dt_pr
            if dt_delta == timedelta(days=1):
                cases_inc = cases - cases_pr
                death_inc = death - death_pr
                moscow_daily.append(cases_inc)
            else:
                print('timedelta error near date {}'.format(str(dt)))
                raise

        dt_pr = dt
        cases_pr = cases
        death_pr = death

        r = [locs, prov, dt, cases, cases_inc, death, death_inc]
        r = [str(i) for i in r]
        r = '|'.join(r)
        dst.write(r + '\n')

print('done')
