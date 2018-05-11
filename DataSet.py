import pandas as pd
import numpy as np
class DataSet(object):
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.grouped = self.df.groupby(self.df.station_id)
        self.dict= dict(list(self.grouped))
    def get_data(self,idname,start_date,end_date=None):
        if(type(idname) ==list):
            res = []
            for id_ in idname:
                temp = self.dict[id_]
                temp.index= pd.to_datetime(temp.utc_time)
                if(end_date==None):
                    res.append(temp[start_date])
                else:
                    res.append(temp[start_date:end_date])
            return res
        else:
            temp = self.dict[idname]
            temp.index= pd.to_datetime(temp.utc_time)
            if(end_date==None):
                return temp[start_date]
            else:
                return temp[start_date:end_date]
    def get_all_ids(self):
        return list(self.dict.keys())
    def get_all_date(self):
        return self.df.utc_time.unique()
    def get_date_range(self):
        return self.df.utc_time.unique()[0],self.df.utc_time.unique()[-1]