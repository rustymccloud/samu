import os
import io
import sys
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

rs_user = ''
rs_pass = ''
rs_host = 'bleh.redshift.thingy.com'
rs_port = 8794
rs_db = 'yerdb'

engine = create_engine(f'postgresql://{rs_user}:{rs_pass}@{rs_host}:{rs_port}/{rs_db}')

df = pd.read_csv('sample.csv', encoding='utf8')

df.to_sql('booker_processor_actuals', engine, schema='_mbanalysis', if_exists='append', index=False)