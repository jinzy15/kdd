#coding=utf-8
import csv
import re  #分词
import numpy as np
import pandas as pd

def get_key (dict, value):
    return [k for k, v in dict.items() if v == value]

def Dict_match(filepath):    
    csv_reader = csv.reader(open(filepath, encoding='utf-8'))
    Dict = {}
    for row in csv_reader:  #0 城区监测点　１　郊区监测点
        Dict[row[0]] = row[1] 
    return Dict

def get_another_factors(file_path, Match_Dict, Mode):  #Mode 0 基于历史数据训练　1　基于当天数据预测    
    #找对应项，构建列表
    csv_reader = csv.reader(open(file_path, encoding='utf-8'))
    #临近气象站点列表
    another_factor = {}
    for s0 in Match_Dict:
        for s1 in csv_reader:
            data_list = []
            station_id = ""
            time = ""
            if Mode == 0:  #训练模式
                station_id = s1[0]
                time = s1[3]
            if Mode == 1:  #预测模式
                station_id = s1[1]
                time = s1[2]
                
            if Match_Dict[s0] == station_id:
                key = s0 + "#" + time
                for i in range(4, 7):
                    data_list.append(s1[i])
                another_factor[key] = data_list    
    return another_factor

def add_factor(file_path, out_file, another_factor, Mode):
    test_reader = csv.reader(open(file_path, encoding='utf-8'))
    #给测试集站点填加温度　湿度信息
    df = pd.read_csv(file_path)
    temper = []
    press  = []
    humi   = []
    for s0 in test_reader:
        station_id = ""
        time = ""
        if Mode == 1:  #测试数据
            station_id = s0[1]
            time = s0[2]
        if Mode == 0:  #训练数据
            station_id = s0[0]
            time = s0[3]
        if station_id == 'station_id' or station_id == 'stationName':
            continue
        key = station_id + "#" + time
        if key in another_factor.keys():
            temper.append(another_factor[key][0])
            press.append(another_factor[key][1])
            humi.append(another_factor[key][2])
        else:  #出现缺失的情况，补一个缺失值
            temper.append(np.nan)
            press.append(np.nan)
            humi.append(np.nan)
    df['temperature'] = temper
    df['pressure'] = press
    df['humidity'] = humi
    df.to_csv(out_file)

def add_out(match_city, file_temp, file_pm2, out_file):
    match_dict = Dict_match(bj_match)  #寻找临近的气象站　match_city: data/match_bj.csv  data/match_ld.csv
    another_factor = get_another_factors(bj_his, match_dict)  #获得湿度信息的列表
    add_factor(bj_aq, out_file, another_factor)  #添加到含pm2.5的文件中