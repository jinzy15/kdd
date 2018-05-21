# coding: utf-8
#config
from add_factor import *
#处理数据 改变时间格式
import pandas as pd
df = pd.read_csv('data/london_aq.csv')
df.utc_time = pd.to_datetime(df.utc_time)
df.to_csv('data/new_london_aq.csv')

temp_file = {'bj':'data/Beijing_historical_meo_grid.csv', 'ld': 'data/London_historical_meo_grid.csv'}
pm2_file = {'bj':'data/beijing_17_18_aq.csv', 'ld': 'data/new_london_aq.csv'}
out_file = {'bj':'data/bj_data.csv', 'ld': 'data/ld_data.csv'}
for city in ['bj','ld']:
    match_city = 'data/match_' + city + '.csv'
    file_temp = temp_file[city]
    file_pm2 = pm2_file[city]
    outfile = out_file[city]
    add_out(match_city, file_temp, file_pm2, outfile, 0, city)  #训练模式