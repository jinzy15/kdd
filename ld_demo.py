import DataSet
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib

##parameters
#we need to constru more factor

factor = ['PM2.5','PM10','NO2']
train_start_date = '2017-01-01'
train_end_date = '2017-09-01'
test_start_date = '2017-09-01'
test_end_date = '2018-01-01'
seq_len = 48
predict_len = 48

def set_to_XY(train):
	X = []
	Y = []
	for i in range(len(train)-seq_len-predict_len):
	    X.append(np.hstack(np.array(train.iloc[i:i+seq_len])))
	    Y.append(np.hstack(np.array(train.iloc[i+seq_len : i+seq_len+predict_len])))
	X = np.array(X)
	Y = np.array(Y)
	return X,Y

def smape(actual, predicted):
    a = np.abs(np.array(actual) - np.array(predicted))
    b = np.array(actual) + np.array(predicted)
    return 2 * np.mean(np.divide(a, b, out=np.zeros_like(a), where=b!=0, casting='unsafe'))

regr = LinearRegression()

mydata = DataSet.DataSet('data/london_aq.csv')
all_ids = mydata.get_all_ids()
print(all_ids)
for item in all_ids:
	print(item)
	temp_train = mydata.get_data(item,train_start_date,train_end_date)
	temp_test =  mydata.get_data(item,test_start_date,test_end_date)

#we need to change this data process way smarter
	temp_train = temp_train.fillna(method = 'ffill')
	temp_train= temp_test.fillna(method = 'bfill')
	temp_train = temp_train[factor]
	# print(np.isnan(temp_train).any())
	# print(temp_train.isnull().any())
	# print(np.isfinite(temp_train).all())

# train

	X,Y =  set_to_XY(temp_train)

	# import ipdb;ipdb.set_trace()
	try:
		regr = regr.fit(X, Y)
	except:
		pass

# test
	temp_test= temp_test.fillna(method = 'ffill')
	temp_test= temp_test.fillna(method = 'bfill')
	temp_test = temp_test[factor]
	# print(np.isnan(temp_test).any())
	# print(temp_test.isnull().any())
	# print(np.isfinite(temp_test).all())
	X,Y =  set_to_XY(temp_test)
	try:
		predict = regr.predict(X)
		sum = 0
		length  = len(Y)
		for yy,pre in zip(Y,predict):
			pre[pre<0] = 0
			sum+=smape(yy,pre)
		print(item,'expect loss is ', sum/length)
	except:
		pass

joblib.dump(regr, "model/ld_train_model.m")





