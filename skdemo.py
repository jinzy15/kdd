import DataSet
import numpy as np

##parameters
#we need to constru more factor
factor = ['PM2.5','PM10','NO2','CO','O3','SO2']
train_start_date = '2017-01-01'
train_end_date = '2017-09-01'
test_start_date = '2017-09-01'
test_end_date = '2018-01-01'
seq_len = 20

def set_to_XY(train):
	X = []
	Y = []
	for i in range(len(train)-seq_len):
	    X.append(np.hstack(np.array(train.iloc[i:i+seq_len])))
	    Y.append(np.array(train.iloc[i+seq_len]))
	X = np.array(X)
	Y = np.array(Y)
	return X,Y

def smape(actual, predicted):
    a = np.abs(np.array(actual) - np.array(predicted))
    b = np.array(actual) + np.array(predicted)
    return 2 * np.mean(np.divide(a, b, out=np.zeros_like(a), where=b!=0, casting='unsafe'))

mydata = DataSet.DataSet('data/beijing_17_18_aq.csv')
aoti_train = mydata.get_data('aotizhongxin_aq',train_start_date,train_end_date)
aoti_test =  mydata.get_data('aotizhongxin_aq',test_start_date,test_end_date)

#we need to change this data process way smarter
aoti_train = aoti_train.fillna(method = 'ffill')
aoti_train = aoti_train[factor]

# train

X,Y =  set_to_XY(aoti_train)

from sklearn.linear_model import LinearRegression
regr = LinearRegression().fit(X, Y)

# test
aoti_test= aoti_test.fillna(method = 'ffill')
aoti_test = aoti_test[factor]
X,Y =  set_to_XY(aoti_test)
predict = regr.predict(X)
print(smape(Y,predict))
