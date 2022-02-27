# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 08:30:05 2022

@author: hp
"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn import linear_model
import numpy as np

import pandas as pd

def data_transformation(data):
    #Encode no of bedrooms column
    enc=OneHotEncoder(handle_unknown='ignore')
    enc_data=pd.DataFrame(enc.fit_transform(data[['bedrooms']]).toarray())
    new_data=data.join(enc_data)
    new_data=new_data.drop(['bedrooms'],axis='columns')
    return(new_data)
def multiple_model(data,bedrooms):
    other_data=[]
    for i in range(len(list(data.columns))-2):
        other_data.append(1)
    data=data_transformation(data)
    target_name ="Price"
    target=data[target_name]
    data=data.drop(columns=[target_name])
    model = linear_model.LinearRegression()
    model.fit(data,target)
    
    bedroom_list=[]
    for b in range(9):
        bedroom_list.append(0)
    bedroom_list[int(bedrooms)-1]=1
    features=other_data+bedroom_list
    x_pred=np.array(features).reshape(1,len(features))
    y_pred=model.predict(x_pred)
    return(int(round(y_pred[0],0)))
