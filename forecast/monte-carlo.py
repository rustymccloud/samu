from ayx import Alteryx

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import norm
%matplotlib inline

import os
import time
import datetime

revenue = Alteryx.read('#1')
revenue.head()

#Define Variables
decline, decline_hist, decline_sim = revenue['decline_driver'].loc[0], revenue['decline_diff'], []
bonus_up, bonus_up_hist, bonus_up_sim = revenue['subrev_upgrade_driver'].loc[0], revenue['subrev_upgrade_diff'], []
bonus_down, bonus_down_hist, bonus_down_sim = revenue['subrev_downgrade_driver'].loc[0], revenue['subrev_downgrade_diff'], []
prem_up, prem_up_hist, prem_up_sim = revenue['premrev_upgrade_driver'].loc[0], revenue['premrev_upgrade_diff'], []
prem_down, prem_down_hist, prem_down_sim = revenue['premrev_downgrade_driver'].loc[0], revenue['premrev_downgrade_diff'], []
tech_up, tech_up_hist, tech_up_sim = revenue['techdist_upgrade_driver'].loc[0], revenue['techdist_upgrade_diff'], []
tech_down, tech_down_hist, tech_down_sim = revenue['techdist_downgrade_driver'].loc[0], revenue['techdist_downgrade_diff'], []
pay_up, pay_up_hist, pay_up_sim = revenue['payrev_expand_driver'].loc[0], revenue['payrev_expand_diff'], []
pay_down, pay_down_hist, pay_down_sim = revenue['payrev_contract_driver'].loc[0], revenue['payrev_contract_diff'], []

def mc(start,hist,sim_out,timeline):
    val = start
    sim_out = []
    for i in range(timeline):
        val += hist.sample(n=1).reset_index(drop=True).loc[0]
        sim_out.append(val)
    return pd.Series(sim_out)

timeline = 12
revenue_end_date = revenue['nre_date'].max()
sim_dates = pd.date_range(start=revenue_end_date, periods=timeline+1, dtype='datetime64[M]', freq='M').values.astype('datetime64[M]')
sim_columns = pd.Series(sim_dates[1:].astype('str')).append(pd.Series(['Driver','Sim'])).tolist()
revenue_base = pd.Series([1,1,1,1,1,1,1,1,1,1,1,1])
revenue_sim = pd.DataFrame(columns=sim_columns)

for i in range(300):
    sim_period = 'sim-'+str(i)
    decline_mc = mc(decline,decline_hist,decline_sim,timeline).append(pd.Series(['decline'])).append(pd.Series(sim_period)).tolist()
    bonus_up_mc = mc(bonus_up,bonus_up_hist,bonus_up_sim,timeline).append(pd.Series(['bonus_up'])).append(pd.Series(sim_period)).tolist()
    bonus_down_mc = mc(bonus_down,bonus_down_hist,bonus_down_sim,timeline).append(pd.Series(['bonus_down'])).append(pd.Series(sim_period)).tolist()
    prem_up_mc = mc(prem_up,prem_up_hist,prem_up_sim,timeline).append(pd.Series(['prem_up'])).append(pd.Series(sim_period)).tolist()
    prem_down_mc = mc(prem_down,prem_down_hist,prem_down_sim,timeline).append(pd.Series(['prem_down'])).append(pd.Series(sim_period)).tolist() 
    tech_up_mc = mc(tech_up,tech_up_hist,tech_up_sim,timeline).append(pd.Series(['tech_up'])).append(pd.Series(sim_period)).tolist()
    tech_down_mc = mc(tech_down,tech_down_hist,tech_up_sim,timeline).append(pd.Series(['tech_down'])).append(pd.Series(sim_period)).tolist()
    pay_up_mc = mc(pay_up,pay_up_hist,pay_up_sim,timeline).append(pd.Series(['pay_up'])).append(pd.Series(sim_period)).tolist()
    pay_down_mc = mc(pay_down,pay_down_hist,pay_down_sim,timeline).append(pd.Series(['pay_down'])).append(pd.Series(sim_period)).tolist()
    revenue_mc = revenue_base + decline_mc[:-2] + bonus_up_mc[:-2] + bonus_down_mc[:-2] + prem_up_mc[:-2] + prem_down_mc[:-2] + tech_up_mc[:-2] + tech_down_mc[:-2] + pay_down_mc[:-2] + pay_up_mc[:-2]
    revenue_mc =  revenue_mc.append(pd.Series(['revenue'])).append(pd.Series(sim_period)).tolist()
    revenue_data = pd.DataFrame([revenue_mc,decline_mc,bonus_up_mc,bonus_down_mc,prem_up_mc,prem_down_mc,tech_up_mc,tech_down_mc,pay_up_mc,pay_down_mc]\
                             , columns=sim_columns).reset_index()
    revenue_sim = revenue_sim.append(revenue_data)
    plt.plot(revenue_mc[:-2])
plt.show()
revenue_sim = revenue_sim.drop(columns='index')

revenue_sim.head()

revenue_sim = pd.melt(revenue_sim,id_vars=['Driver','Sim'],value_vars=sim_columns[:-2])
revenue_sim=revenue_sim.rename(columns = {'variable':'revenue_date'})
revenue_sim['revenue_date'] = revenue_sim['revenue_date']+'-01'

hist_append = revenue.iloc[:,0:10].head(24)
hist_append.columns = ['revenue_date','decline','bonus_up','bonus_down','prem_up','prem_down','tech_up','tech_down','pay_up','pay_down']
hist_append['revenue']=1+hist_append['decline']+hist_append['bonus_up']+hist_append['bonus_down']+hist_append['prem_up']+hist_append['prem_down']+hist_append['tech_up']+hist_append['tech_down']+hist_append['pay_up']+hist_append['pay_down']
hist_append = pd.melt(hist_append,id_vars=['revenue_date'],value_vars=hist_append.columns[1:])
hist_append.columns = ['revenue_date','Driver','value']
hist_append['Sim']='historical'
hist_append['revenue_date'] = pd.to_datetime(hist_append['revenue_date']).astype('str')
hist_append =  hist_append[['Driver','Sim','revenue_date','value']]

revenue_out = revenue_sim.append(hist_append)
Alteryx.write(revenue_out,1)