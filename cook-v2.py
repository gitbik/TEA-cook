from functools import total_ordering
import streamlit as st
import pandas as pd
import numpy as np
from decimal import *
import openpyxl

def decimal_from_value(value):
    return Decimal(value)

# CSS to inject contained in a string
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
### Inject CSS with Markdown

state_name = pd.read_csv("states.csv")
el_price = pd.read_excel("el_price_rev.xlsx")

#Household Profile
with st.sidebar:
	st.header("Household Profile")
	adults = st.slider('Adults', min_value=1, max_value=5, value=None, step=1)  # slider widget to select family members
	st.write('Number of Adults in the Household -', adults)
	children = st.slider('Children', min_value=0, max_value=5, value=None, step=1)  # slider widget to select family members
	st.write('Number of Children in the Household -', children)
	st.write('*Total number of persons in the Household* -', adults+children)
	area_select =  st.selectbox('Area Type',('Urban','Rural'))
	soc_eco_select= st.selectbox('Socio-Economic Status',('Lower','Middle','Higher'))
	state_select = st.selectbox('State',state_name)
	hh_size = adults + children

# Primary Cooking Fuel Selection

## edits required - urban selection - fuels available - LPG and PNG
## rural selection - fuels available - Firewood, Biogas and LPG

with st.expander('1\) Select Baseline Cooking Scenario'):
	#st.header('Baseline Scenario')
	df_base_cf = pd.read_excel("cook-fuel-stove.xlsx",sheet_name="baseline") ##area_select
	df_base_cf2 = df_base_cf.loc[(df_base_cf['Area'] == area_select) & (df_base_cf['Socio-Economic'] == soc_eco_select)]
	df_base_cf1 = df_base_cf2["Fuel"].drop_duplicates()
	bpf_select = st.selectbox('Primary Cooking Fuel',(df_base_cf1))
	mask_bf_stv = df_base_cf['Fuel'].isin([bpf_select])
	df_base_cf_st = df_base_cf2[mask_bf_stv].iloc[:,2]

	prst_select = st.selectbox('Primary Cookstove', (df_base_cf_st))
	prst_stack_percent = st.slider('% of cooking done with the primary cookstove',min_value = 50, max_value = 100, step = 10, value = 100)

# Electric Cooking Selection
with st.expander('2\) Select Electric Cooking Scenario'):
	#st.header('e-Cooking Scenario')
	df_elec_cf = pd.read_excel("cook-fuel-stove.xlsx",sheet_name="e-cooking")
	df_elec_cf2 = df_elec_cf.loc[(df_elec_cf['Area'] == area_select) & (df_elec_cf['Socio-Economic'] == soc_eco_select)]
	df_elec_cf1 = df_elec_cf2["Fuel"].drop_duplicates()
	epf_select = st.selectbox('Electricity Source', (df_elec_cf1))
	mask_ef_stv = df_elec_cf['Fuel'].isin([epf_select])
	df_elec_cf_st = df_elec_cf2[mask_ef_stv].iloc[:,2]
	est_sel = st.selectbox('e-Cooking Appliance',(df_elec_cf_st))
	est_stack_percent = st.slider('% of total cooking to be done', min_value = 50, max_value = 100, step = 10)
	
# Cooking Pattern
df_region = pd.read_excel("region-cooking.xlsx")

with st.expander('3\) Cooking Pattern'):
	#st.markdown('Region & Cuisine')
	mask = df_region['States'].str.contains(state_select, case=False, na=False)
	st.dataframe(df_region[mask].iloc[:,0:1],width=120)
	st.table(df_region[mask].iloc[:,2:3])

	st.markdown('Daily Cooking Pattern')
	df_dail_cook = df_region.iloc[:3,4:]
	st.dataframe(df_dail_cook)

# Convert the DataFrame to an HTML table without the index column
#table = df_dail_cook.to_html(index=False)

# Display the HTML table in Streamlit
#st.write(table, unsafe_allow_html=True)

# Results - Cooking Techno-economic analysis

with st.expander('4\) Results  \- Cookstove Characteristics'):
	#baseline stove charactersitics
	df_base_cf4 = df_base_cf2.loc[(df_base_cf2['Stove'] == prst_select)]
	bs_life = df_base_cf4['Life'].values[0]
	bs_eff = (df_base_cf4['Thermal Efficiency'].values[0]) *100
	bs_capex = df_base_cf4['Capex'].values[0]
	bs_opex = df_base_cf4['Overheads (Stove)'].values[0]
	bs_tcost = bs_capex + bs_opex

	#electric stove characteristics
	df_el_cf4 = df_elec_cf2.loc[(df_elec_cf2['Stove'] == est_sel) & (df_elec_cf2['Fuel'] == epf_select)]
	#df_el_cf4 = df_elec_cf2.loc[df_elec_cf2['Stove'] == est_sel]
	el_life = df_el_cf4['Life'].values[0]
	el_eff = (df_el_cf4['Thermal Efficiency'].values[0]) *100
	el_capex = df_el_cf4['Capex'].values[0]
	el_opex = df_el_cf4['Overheads (Stove)'].values[0]
	el_tcost = el_capex + el_opex
	
	#dataframe - cookstove characteristics
	cst_var  = {'Variable':['Type','Life','Thermal Efficiency', 'Capex', 'Overheads', 'Total Cost'],
	'Units':['-','Years','%','INR','INR/year','INR'],
	'Baseline':[prst_select,bs_life.round(0),bs_eff.round(0),bs_capex,bs_opex,bs_tcost],
	'e-Cooking':[est_sel,el_life.round(0),el_eff.round(0),el_capex,el_opex,el_tcost],
	'Delta':['-',(el_life-bs_life).round(0),(el_eff - bs_eff).round(0),(el_capex - bs_capex).round(0),(el_opex - bs_opex).round(0),(el_tcost-bs_tcost).round(0)]
	}
	df_cst_var = pd.DataFrame(cst_var)
	st.dataframe(df_cst_var)

# Results - Energy Demand)

with st.expander('5\) Results  \- Energy Demand & Cost'):
	#baseline energy demand
	## daily cooking duration
	if hh_size < 3:
		bs_dcd = (df_base_cf4['Daily cooking duration'].values[0].round(2))* 0.75
	elif hh_size <= 6:
		bs_dcd = df_base_cf4['Daily cooking duration'].values[0].round(2)
	else:
		bs_dcd = (df_base_cf4['Daily cooking duration'].values[0].round(2)) * 1.25
	#bs_dcd = df_base_cf4['Daily cooking duration'].values[0].round(2)
	bs_hc = df_base_cf4['Hourly consumption'].values[0]
	#bs_dc = df_base_cf4['Daily consumption'].values[0]
	bs_dc = (bs_dcd * bs_hc)
	bs_ac = bs_dc * 365 * 0.9
	#electric demand
	if hh_size < 3:
		el_dcd = (df_el_cf4['Daily cooking duration'].values[0].round(2))* 0.75
	elif hh_size <= 6:
		el_dcd = df_el_cf4['Daily cooking duration'].values[0].round(2)
	else:
		el_dcd = (df_el_cf4['Daily cooking duration'].values[0].round(2)) * 1.25
	#el_dcd = df_el_cf4['Daily cooking duration'].values[0].round(2)
	el_hc = df_el_cf4['Hourly consumption'].values[0]
	el_dc = el_dcd * bs_hc
	el_ac = el_dc * 365 * 0.9

	#dataframe - energy demand
	encons_var  = {'Variable':['Daily cooking duration', 'Hourly consumption', 'Daily consumption', 'Annual consumption'],
	'Units':['hours/day','kWh/hour','kWh/day','kWh/year'],
	'Baseline':	[bs_dcd.round(2),bs_hc.round(2),bs_dc.round(2),(bs_dc * 365 * 0.9).round(2)],
	'e-Cooking':[el_dcd.round(2),el_hc,el_dc.round(2),el_ac.round(2)],
	'Delta':[(el_dcd - bs_dcd).round(2),(el_hc - bs_hc).round(2),(el_dc - bs_dc).round(2),(el_ac - bs_ac).round(2)]
	}
	df_encons_var = pd.DataFrame(encons_var)
	df_encons_var_round = df_encons_var.round(2)
	#st.dataframe(df_encons_var)

# with st.expander('6\) Results  \- Energy Cost'):
	#baseline - energy cost
	bs_uc = df_base_cf4['Unit cost'].values[0] #unit cost
	bs_opc = df_base_cf4['Opex'].values[0] #opex
	bs_ovc = df_base_cf4['Overheads (Fuel)'].values[0] #overheads
	bs_etc = bs_opc + bs_ovc #total cost

	#electric cost
	el_price2 = el_price[['State',soc_eco_select]] #filtering dataframe
	el_price3 = el_price2.loc[el_price2['State'] == state_select,soc_eco_select] #unit cost
	el_uc = el_price3.item()
	#el_uc = df_el_cf4['Unit cost'].values[0]
	el_opc = df_el_cf4['Opex'].values[0] #opex
	el_ovc = df_el_cf4['Overheads (Fuel)'].values[0] #overheads
	el_etc = el_opc + el_ovc #total cost

	#dataframe - energy cost
	encost_var  = {'Variable':['Unit cost', 'Opex', 'Overheads', 'Total cost'],
	'Units':['INR/kWh','INR/year','INR/year','INR/year'],
	'Baseline':[bs_uc,bs_opc.round(2),bs_ovc,bs_etc.round(2)],
	'e-Cooking':[el_uc,el_opc.round(2),el_ovc,el_etc.round(2)],
	'Delta':[(el_uc - bs_uc).round(2),(el_opc - bs_opc).round(2),(el_ovc - bs_ovc).round(2),(el_etc - bs_etc).round(2)]
	}
	df_encost_var = pd.DataFrame(encost_var)
	df_tcost = pd.concat([df_encons_var,df_encost_var], ignore_index=True)
	df_tcost = df_tcost.astype(str)
	#df_tcost = df_tcost.applymap(lambda x: "{:.2f}".format(x))
	#st.write(df_tcost)
	st.dataframe(df_tcost)

with st.expander('6\) Results  \- Health Impacts'):
	#baseline - health impacts
	bs_dihap = df_base_cf4['Daily IHAP (PM2.5)'].values[0]
	#bs_ahap = bs_dihap * 365 * 0.9
	bs_ahap = df_base_cf4['Annual IHAP (PM2.5)'].values[0]
	bs_haz = df_base_cf4['Health Hazard'].values[0]
	bs_mort = df_base_cf4['Mortality Estimates'].values[0]

	#electric - health impacts
	el_dihap = df_el_cf4['Daily IHAP (PM2.5)'].values[0]
	#el_ahap = el_dihap * 365 * 0.9
	el_ahap = df_el_cf4['Annual IHAP (PM2.5)'].values[0]
	el_haz = df_el_cf4['Health Hazard'].values[0]
	el_mort = df_el_cf4['Mortality Estimates'].values[0]

	#dataframe - health impacts
	hlt_var  = {'Variable':['Daily IHAP (PM 2.5)','Annual IHAP (PM 2.5)','Health Hazard','Averted Premature Mortality'],
	'Units':['μg/m3','mg/m3','-','% or no.'],
	'Baseline':[bs_dihap.round(2),bs_ahap.round(2),bs_haz,bs_mort],
	'e-Cooking':[el_dihap.round(2),el_ahap.round(2),el_haz,el_mort],
	'Delta':[(el_dihap - bs_dihap).round(2),(el_ahap - bs_ahap).round(2) ,'-','-']
	}
	df_hlt_var = pd.DataFrame(hlt_var).round(2)
	#st.dataframe(df_hlt_var)
	st.write(df_hlt_var)

with st.expander('7\) Results  \- Financing'):
	#baseline - financing
	bs_aninc = df_base_cf4['Annual Income'].values[0]
	bs_pbp = df_base_cf4['Payback period'].values[0]
	bs_uce = df_base_cf4['Unit carbon emission'].values[0]
	bs_ucc = df_base_cf4['Unit cost of carbon credit (CC)'].values[0]
	bs_tce = df_base_cf4['Total carbon emissions (FS+EI*)'].values[0]
	bs_tcrp = df_base_cf4['Total CC revenue possible'].values[0]

	#electric - financing
	el_aninc = df_el_cf4['Annual Income'].values[0]
	#el_pbp = df_el_cf4['Payback period'].values[0]
	el_pbp = (el_capex)/((bs_etc - el_etc) + (bs_opex - el_opex))
	el_uce = df_el_cf4['Unit carbon emission'].values[0]
	el_ucc = df_el_cf4['Unit cost of carbon credit (CC)'].values[0]
	el_tce = df_el_cf4['Total carbon emissions (FS+EI*)'].values[0]
	#el_tcrp = df_el_cf4['Total CC revenue possible'].values[0]	
	el_tcrp = ((bs_tce - el_tce) * el_ucc)

	fin_var  = {'Variable':['Annual Income of HH','Payback period','Unit carbon emission','Total carbon emissions (FS+EI*)','Unit cost of carbon credit (CC)','Total CC revenue possible'],
	'Units':['INR','years','MtCO2eq./kWh','MtCO2eq./year','INR/MtCO2eq.','INR/year'],
	'Baseline':[bs_aninc,'-',bs_uce,bs_tce.round(2),'-','-'],
	'e-Cooking':['NA',el_pbp.round(2),el_uce.round(2),el_tce.round(2),el_ucc,el_tcrp.round(2)],
	'Delta':['-','-',(el_uce - bs_uce).round(2),(el_tce - bs_tce).round(2),'-','-']
	}
	df_fin_var = pd.DataFrame(fin_var)
	st.dataframe(df_fin_var)
	st.markdown('FS - Fuel Switch, EI - Efficiency Improvement')

st.markdown('<mark>*This is a draft version. Values mentioned are based on research papers and empirical evidence.*</mark>', unsafe_allow_html=True)

st.markdown('<mark>*This analysis is a part of Deep Electrification initiative ideated by Vasudha Foundation and supported by SED Fund. For any queries, collaboration or further use of this research. Please drop a mail to bikash@vasudhaindia.org*</mark>', unsafe_allow_html=True)

# 1 - create a data frame with the variables
# 2 - append the units to the data frame
# 3 - create baseline dataframe - with default values + based on user input values
# 4 - append to the previous table created
# 5 - create electric cooking dataframe
# 6 - append to the previous table
# 7 - create difference dataframe b/w baseline and electric cooking
# 8 - append difference df to the main df