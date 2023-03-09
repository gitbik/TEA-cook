import streamlit as st
import pandas as pd
import numpy as np
from decimal import *

df_base_cf = pd.read_excel("cook-fuel-stove.xlsx",sheet_name="baseline") ##area_select
df_base_cf2 = df_base_cf.loc[(df_base_cf['Area'] == 'Urban') & (df_base_cf['Socio-Economic'] == 'Lower')]
df_base_cf1 = df_base_cf2["Fuel"].drop_duplicates()
#bpf_select = st.selectbox('Primary Cooking Fuel',(df_base_cf1))
#mask_bf_stv = df_base_cf['Fuel'].isin([bpf_select])
#df_base_cf_st = df_base_cf2[mask_bf_stv].iloc[:,2]
#prst_select = st.selectbox('Primary Cookstove', (df_base_cf_st))
#prst_stack_percent = st.slider('% of cooking done with the primary cookstove',min_value = 50, max_value = 100, step = 10)

df_elec_cf = pd.read_excel("cook-fuel-stove.xlsx",sheet_name="e-cooking")
df_elec_cf2 = df_elec_cf.loc[(df_elec_cf['Area'] == 'Urban') & (df_elec_cf['Socio-Economic'] == 'Lower')]
df_elec_cf1 = df_elec_cf2["Fuel"].drop_duplicates()
#epf_select = st.selectbox('Electricity Source', (df_elec_cf1))
#mask_ef_stv = df_elec_cf['Fuel'].isin([epf_select])
#df_elec_cf_st = df_elec_cf2[mask_ef_stv].iloc[:,2]
#est_sel = st.selectbox('e-Cooking Appliance',(df_elec_cf_st))
#   est_stack_percent = st.slider('% of total cooking to be done', min_value = 50, max_value = 100, step = 10)

#baseline stove charactersitics
df_base_cf4 = df_base_cf2.loc[(df_base_cf2['Stove'] == 'Traditional cook stove (TCS)')]
bs_life = df_base_cf4['Life'].values[0]
bs_eff = (df_base_cf4['Thermal Efficiency'].values[0])*100
bs_capex = df_base_cf4['Capex'].values[0]
bs_opex = df_base_cf4['Overheads (Stove)'].values[0]
bs_tcost = bs_capex + bs_opex

#electric stove characteristics
df_el_cf4 = df_elec_cf2.loc[(df_elec_cf2['Stove'] == est_sel) & (df_elec_cf2['Fuel'] == epf_select)]
#df_el_cf4 = df_elec_cf2.loc[df_elec_cf2['Stove'] == est_sel]
el_life = df_el_cf4['Life'].values[0]
el_eff = (df_el_cf4['Thermal Efficiency'].values[0])*100
el_capex = df_el_cf4['Capex'].values[0]
el_opex = df_el_cf4['Overheads (Stove)'].values[0]
el_tcost = el_capex + el_opex

prst_select = 'Traditional cook stove (TCS)'

#dataframe - cookstove characteristics
cst_var  = {'Variable':['Type','Life','Thermal Efficiency', 'Capex', 'Overheads', 'Total Cost'],
'Units':['-','Years','%','INR','INR/year','INR'],
'Baseline':[prst_select,bs_life,bs_eff,bs_capex,bs_opex,bs_tcost],
'e-Cooking':[est_sel,el_life,el_eff,el_capex,el_opex,el_tcost],
'Delta':['-',(el_life-bs_life),(el_eff - bs_eff),(el_capex - bs_capex),(el_opex - bs_opex),(el_tcost-bs_tcost)]
}
df_cst_var = pd.DataFrame(cst_var)
#st.dataframe(df_cst_var)

# Electric Cooking Selection
	#st.header('e-Cooking Scenario')
df_elec_cf = pd.read_excel("cook-fuel-stove.xlsx",sheet_name="e-cooking")
df_elec_cf2 = df_elec_cf.loc[(df_elec_cf['Area'] == 'Urban') & (df_elec_cf['Socio-Economic'] == 'Lower')]
df_elec_cf1 = df_elec_cf2["Fuel"].drop_duplicates()
#epf_select = st.selectbox('Electricity Source', (df_elec_cf1))
mask_ef_stv = df_elec_cf['Fuel'].isin([epf_select])
df_elec_cf_st = df_elec_cf2[mask_ef_stv].iloc[:,2]
#est_sel = st.selectbox('e-Cooking Appliance',(df_elec_cf_st))
est_stack_percent = st.slider('% of total cooking to be done', min_value = 50, max_value = 100, step = 10)

with st.expander('5\) Results  \- Energy Demand'):
#baseline energy demand
    bs_dcd = df_base_cf4['Daily cooking duration'].values[0]
    bs_hc = df_base_cf4['Hourly consumption'].values[0]
    #bs_dc = df_base_cf4['Daily consumption'].values[0]
    bs_dc = (bs_dcd * bs_hc)
    bs_ac = bs_dc * 365 * 0.9
    #electric demand
    el_dcd = df_el_cf4['Daily cooking duration'].values[0].round(2)
    el_hc = df_el_cf4['Hourly consumption'].values[0]
    el_dc = el_dcd * bs_hc
    el_ac = el_dc * 365 * 0.9

    #dataframe - energy demand
    encons_var  = {'Variable':['Daily cooking duration', 'Hourly consumption', 'Daily consumption', 'Annual consumption'],
    'Units':['hours/day','kWh/hour','kWh/day','kWh/year'],
    'Baseline':	[bs_dcd,bs_hc,bs_dc,bs_dc * 365 * 0.9],
    'e-Cooking':[el_dcd,el_hc,el_dc,el_ac],
    'Delta':[(el_dcd - bs_dcd),(el_hc - bs_hc),(el_dc - bs_dc),(el_ac - bs_ac)]
    }
    df_encons_var = pd.DataFrame(encons_var)
    st.dataframe(df_encons_var)

