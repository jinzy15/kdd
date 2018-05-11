import pandas as pd
import numpy as np
def add_ab(file_a,file_b,file_c):
	a = pd.read_csv(file_a)
	b = pd.read_csv(file_b)
	dict_a = {}
	dict_b = {}
	for i,j in a.groupby(a['stationId']):
	    dict_a[i]=j
	for i,j in b.groupby(b['stationId']):
	    dict_b[i]=j
	add_dict = {}
	for i in dict_a.keys():
	    dict_a[i].index = dict_a[i].utc_time
	    dict_b[i].index = dict_b[i].utc_time
	    add_dict[i] = pd.concat([dict_a[i],dict_b[i]],join="outer")
	add_df = pd.DataFrame()
	
	for i in add_dict.keys():
		add_df = add_df.append(add_dict[i])
	add_df.index = np.arange(len(add_df))
	add_df.to_csv(file_c)