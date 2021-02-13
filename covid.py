# Module for importing covid-19 case data into pandas dataframe.
# Data source is Covid Tracking Project: https://covidtracking.com

import numpy as no
import pandas as pd

src_name = 'all-states-history.csv'
src = open(src_name, 'r', encoding='utf8')
df = pd.read_csv(src)

df = df.astype({
    'date': 'datetime64[ns]',
    'state': 'string',
    'dataQualityGrade': 'string'
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
    # 'totalTestsViralIncrease': 'int64'
    })


