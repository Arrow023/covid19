from flask import (Flask,render_template,Response,jsonify)
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import datetime as dt
from datetime import date
import numpy as np
import math
import requests

def modeller():
    global model
    X = tn.iloc[:, :-1].values
    y = tn.iloc[:, 1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    model = linear_model.LinearRegression().fit(X_train,y_train)

model=0
app = Flask(__name__) 
data=pd.read_csv('StatewiseTestingDetails.csv')
tn=data[data['State']=='Tamil Nadu']
tn["Date"] = pd.to_datetime(tn["Date"]).dt.strftime("%Y%m%d")
tn['Date']=tn['Date'].astype(int)
tn=tn.drop(['State','TotalSamples','Negative'],axis=1)
tn=tn[tn['Date']>20200600]
for i in range(0,len(tn)+1):
    tn['Date'][i:i+1]=(i+1)**2
modeller()


def updater(tn):
    global date
    current=dt.datetime.now()
    y=int(current.strftime("%Y"))
    m=int(current.strftime("%m"))
    d=int(current.strftime("%d"))
    f_date = date(2020, 6, 1)
    l_date = date(y, m, d)
    delta = l_date - f_date
    delta = delta.days
    fetched=tn[len(tn)-1:len(tn)]['Date']
    final_row=int(math.sqrt(fetched))
    if final_row==delta:
        return tn
    req = requests.get('https://api.covidindiatracker.com/state_data.json')
    response=req.json()
    cases=response[1]['confirmed']
    new_date=delta**2
    new_frame = pd.DataFrame([{'Date':new_date,"Positive":cases}])
    tn=pd.concat([tn,new_frame])
    return tn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update')
def update():
    global tn
    tn=updater(tn)
    modeller()
    return jsonify(status='Model updated successfully')

@app.route('/predict/<data>') 
def predict(data):
    global model
    data=str(math.ceil(model.predict([[int(data)**2]])))
    return jsonify(prediction=data)

if __name__=='__main__':
    app.run()
