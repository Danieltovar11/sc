# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 15:27:08 2020

@author: Daniel Tovar
"""
import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(
      '== Speed Comparison =='
      )

ballast_leg = input('Will the vessel ballast? (yes or no)?: ')

#Ballast yes or no
if ballast_leg == 'yes':
    ballast_distance = float(input('Ballast distance: '))
    ballast_speed = float(input('Ballast speed: '))
    ballast_consumption = float(input('Ballast Consumption: '))
    ballast_time = (ballast_distance / (ballast_speed*24))
    ballast_TTL_consumption = ballast_time * ballast_consumption
else:
    ballast_distance = 0
    ballast_speed = 1
    ballast_consumption = 0
    ballast_time = 0
    ballast_TTL_consumption = 0

"""Creating DataFrame"""
df_bunkers = pd.DataFrame(columns=[
    'Option','Speed','IFO Consumed', 'IFO Cost','LSMGO Consumed','LSMGO Cost','Total Bunker Cost']) 

df_total = pd.DataFrame(columns=['Option','Speed','Duration','Total Hire','TCE','P&L'])

"""Inputs"""
#HIRE & DISTANCES
hire = float(input('Daily hire: '))
laden_distance = float(input('Full Laden Distance: '))
ECA_distance = float(input('ECA distance: '))
#Bunker Prices
ifo_price = float(input('LSO or IFO Price: '))
lsmgo_price = float(input('LSG Price: '))
#Port Bunkers
port_eca = input('LSMGO to be used at port? (yes or no): ')
if port_eca == 'yes':
    port_days_lsmgo = float(input('Port days using LSMGO: '))
    avrg_port_lsmgo = float(input('Average daily LSMGO consumption: '))
    port_days_ifo = float(input('Port days using IFO/VLSFO: '))
    avrg_port_ifo = float(input('Average port daily IFO/VLSFO consumption: '))
else:
    port_days_lsmgo = 0
    avrg_port_lsmgo = 0
    port_days_ifo = float(input('Port days using IFO/VLSFO: '))
    avrg_port_ifo = float(input('Average port daily IFO/VLSFO consumption: '))
#P&L
revenue = float(input('Freight less Comm: '))
cost_less_bunkers = float(input('Costs less Bunkers: '))

"""Options"""
number_of_options = int(input('Number of options to be calculated: '))

#INPUTS
for i in range (number_of_options):
    print (
        '== Option', i+1, ' =='
        )

    laden_speed = float(input('Laden Speed: '))
    laden_consumption = float(input('Consumption at above speed: '))
    extra_rev = float(input('Extra revenue (0 if none, - if negative): '))
    
    
    #calculating
    #IFO/VLSFO CALCS
    laden_ifo = ((laden_distance-ECA_distance)/(laden_speed*24))*laden_consumption
    port_ifo = port_days_ifo * avrg_port_ifo
    TTL_ifo = ballast_TTL_consumption + laden_ifo + port_ifo
    TTL_ifo_cost = TTL_ifo * ifo_price
    
    #LSMGO CALCS
    if ECA_distance == 0:
        laden_lsmgo = 0
    else:
        laden_lsmgo = (ECA_distance/(laden_speed*24))*laden_consumption
    
    port_lsmgo = port_days_lsmgo * avrg_port_lsmgo
    TTL_lsmgo = laden_lsmgo + port_lsmgo
    TTL_lsmgo_cost = TTL_lsmgo * lsmgo_price
    
    #TTL Bunker Cost
    TTL_bunker_cost = TTL_ifo_cost + TTL_lsmgo_cost
    
    #Time & Hire CALCS
    sailing_time = (laden_distance/(laden_speed*24)) + (ballast_distance/(ballast_speed*24))
    TTL_time  = sailing_time + port_days_ifo + port_days_lsmgo
    TTL_hire = hire * TTL_time
    
    #Totals
    TTL_cost = TTL_bunker_cost + cost_less_bunkers
    TCE = (revenue - TTL_cost) / TTL_time
    P_and_L = profit_and_loss = (revenue - (TTL_cost + TTL_hire)) + extra_rev
    
    """Pandas"""
    opt = i + 1
    df_bunkers.loc[i,['Option']] = opt
    df_bunkers.loc[i,['Speed']] = laden_speed
    df_bunkers.loc[i,['IFO Consumed']] = TTL_ifo
    df_bunkers.loc[i,['IFO Cost']] = TTL_ifo_cost
    df_bunkers.loc[i,['LSMGO Consumed']] = TTL_lsmgo
    df_bunkers.loc[i,['LSMGO Cost']] = TTL_lsmgo_cost
    df_bunkers.loc[i,['Total Bunker Cost']] = TTL_bunker_cost
    
    df_total.loc[i,['Option']] = opt
    df_total.loc[i,['Speed']] = laden_speed
    df_total.loc[i,['Duration']] = TTL_time
    df_total.loc[i,['Total Hire']] = TTL_hire
    df_total.loc[i,['TCE']] = TCE
    df_total.loc[i,['P&L']] = P_and_L
    
df_bunkers.set_index('Option',inplace=True)
df_total.set_index('Option',inplace=True)

print(df_bunkers)
print(df_total)

mini_TCE = (df_total[['TCE']].min())/4
mini_PL = (df_total[['P&L']].min())/4

G1 = df_total.plot.bar(x='Speed',y='P&L',style='ggplot',figsize=(12,8),title='Speed & P&L')
G2 = df_total.plot.bar(x='Speed',y='TCE',color='red',figsize=(12,8),title='Speed & TCE',ylim=[(mini_TCE),(mini_TCE*1.2)])




    
    
