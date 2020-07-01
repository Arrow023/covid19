from flask import Flask
import csv
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import datetime as dt
import numpy as np
import math

app = Flask(__name__) 

data=pd.read_csv('StatewiseTestingDetails.csv')
tn=data[data['State']=='Tamil Nadu']
tn["Date"] = pd.to_datetime(tn["Date"]).dt.strftime("%Y%m%d")
tn['Date']=tn['Date'].astype(int)
tn=tn.drop(['State','TotalSamples','Negative'],axis=1)
tn=tn[tn['Date']>20200600]
X = tn.iloc[:, :-1].values
y = tn.iloc[:, 1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
model = linear_model.LinearRegression().fit(X_train,y_train)

@app.route('/<data>') 
def predict(data):
    return str(math.ceil(model.predict([[int(data)]])))
app.run()
