# coding: utf-8
#config
import pandas as pd
import numpy as np
from add_factor import *
description = 'chai hua submit'
ld_model_path = "model/ld_train_model.m"
bj_model_path = "model/train_model.m"
import datetime
end_time = datetime.datetime.now().strftime('%Y-%m-%d-23')
pred_day = datetime.datetime.now().day+1
start_time = '2018-05-01-00'
import os
file_dir = 'submission/5.'+str(pred_day)+'/'
os.system('mkdir '+file_dir)

# def predict_ans(bj_model_path,ld_model_path):
#     from sklearn.linear_model import LinearRegression
#     from sklearn.externals import joblib
#     regr = joblib.load(bj_model_path)
#     ans = {}
#     bj_now = pd.read_csv(file_dir+'bjnow.csv')
#     bj_now = bj_now.fillna(method = 'ffill')
#     bj_now = bj_now.fillna(method = 'bfill')
#     for i,j in bj_now.groupby(bj_now['station_id']):
#         x = np.hstack(np.array(j.iloc[-48:][['PM25_Concentration','PM10_Concentration','NO2_Concentration','CO_Concentration','O3_Concentration', 'SO2_Concentration' ]]))
#         y = regr.predict(x.reshape(1,-1))
#         ans[i] = y
#     ld_regr = joblib.load(ld_model_path)
#     ld_now = pd.read_csv(file_dir+'ldnow.csv')
#     ld_now = ld_now.fillna(method = 'ffill')
#     ld_now = ld_now.fillna(method = 'bfill')
#     for i,j in ld_now.groupby(ld_now['station_id']):
#         x = np.hstack(np.array(j.iloc[-48:][['PM25_Concentration','PM10_Concentration','NO2_Concentration']]))
#         y = ld_regr.predict(x.reshape(1,-1))
#         ans[i] = y
#     return ans




# In[33]:

from urllib import request
for city in ['bj','ld']:
    url = 'https://biendata.com/competition/airquality/'+city+'/'+start_time+'/'+end_time+'/2k0d1d8' #网页地址
    wp = request.urlopen(url) #打开连接
    content = wp.read() #获取页面内容
    fp = open(file_dir+city+".csv","w+b") #打开一个文本文件
    fp.write(content) #写入数据
    fp.close() #关闭文件
    #柴华君　功能：获取含温度等数据的文件，并保存到city_me.csv中
    url = 'https://biendata.com/competition/meteorology/'+city +'_grid'+'/'+start_time+'/'+end_time+'/2k0d1d8' #网页地址
    print(url)
    wp = request.urlopen(url) #打开连接
    content = wp.read() #获取页面内容
    fp = open(file_dir+city+"_me.csv","w+b") #打开一个文本文件
    fp.write(content) #写入数据
    fp.close() #关闭文件

# In[34]:

import pandas as pd
for city in ['bj','ld']:
    now = pd.read_csv(file_dir+city+'.csv')
    data = pd.DataFrame()
    for i,j in now.groupby(now['station_id']):
        j = j.sort_values(by=['time'])
        data = data.append(j)
        data.to_csv(file_dir+city+'now.csv')

    #柴华君　功能：将温度等数据添加到含no2等空气质量数据的表格中，并保存为city_deal.csv中
    match_city = 'data/match_' + city + '.csv'
    file_temp = file_dir+city+'_me.csv'
    file_pm2 = file_dir+city+'now.csv'
    out_file = file_dir+city+'_deal.csv'
    add_out(match_city, file_temp, file_pm2, out_file, 1)


# ans = predict_ans(bj_model_path,ld_model_path)

# submit2histdata={} 
# for i in list(ans.keys()):
#     submit2histdata[i] = i
# submit2histdata['wanshouxig_aq'] = 'wanshouxigong_aq'
# submit2histdata['aotizhongx_aq'] = 'aotizhongxin_aq'
# submit2histdata['nongzhangu_aq'] = 'nongzhanguan_aq'
# submit2histdata['fengtaihua_aq'] = 'fengtaihuayuan_aq'
# submit2histdata['miyunshuik_aq'] = 'miyunshuiku_aq'
# submit2histdata['yongdingme_aq'] = 'yongdingmennei_aq'
# submit2histdata['xizhimenbe_aq'] = 'xizhimenbei_aq'
# def split_id(input):
#     item,num = input.split('#')
#     return item,num

# submit_csv = pd.read_csv('data/sample_submissioin.csv')
# submit_data = np.array(submit_csv)

# for i in range(len(submit_csv)):
#     item,num = split_id(submit_csv.iloc[i].test_id)
#     try:
#         if(ans[submit2histdata[item]].shape[1]>200):
#             submit_data[i][1:4]=ans[submit2histdata[item]].reshape(48,6)[int(num)][0:3]
#         else:
#             submit_data[i][1:4]=ans[submit2histdata[item]].reshape(48,3)[int(num)]
#     except:
#         pass
# submit = pd.DataFrame(submit_data,columns=submit_csv.columns,index=submit_csv.test_id)
# submit = submit.drop('test_id',1)
# submit[submit<0] = 0
# submit.to_csv(file_dir+'submit.csv')

# import requests

# files={'files': open(file_dir+'submit.csv','rb')}

# data = {
#     "user_id": "kimzenu",   #user_id is your username which can be found on the top-right corner on our website when you logged in.
#     "team_token": "dda0730d880c3e82fea1be19a90335d7776403407ecdee30878f5a1c655ae53a", #your team_token.
#     "description": description ,  #no more than 40 chars.
#     "filename": "submit.csv", #your filename
# }
# url = 'https://biendata.com/competition/kdd_2018_submit/'
# response = requests.post(url, files=files, data=data)
# print(response.text)

