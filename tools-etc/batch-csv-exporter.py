import pandas as pd
import numpy as np

input = pd.read_csv('data/fleet-batch-data.csv')
row_limit = 100
proj_name = 'fleet_vehicles'

input['batch'] = np.ceil((input.index+1)/100).astype(int)

for i in input['batch'].unique():
    df = input[input['batch']==i]
    df['id'].to_csv('data/batch/'+proj_name+'_batch_'+str(i)+'.csv',index=False)