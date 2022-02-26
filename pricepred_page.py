# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 11:05:32 2022

@author: hp
"""

import streamlit as st
import geopandas as gp
import pandas as pd
from model import multiple_model

def main_page():
    data=gp.read_file('shp/buildings.shp')
    bedrooms=list(data.bedrooms.unique())
    bedrooms.sort()
    bedrooms.insert(0,'Select No of bedrooms')
    st.subheader('Price Estimation')
    st.markdown('**Check Desired Property Features**')
    features=['Garden','Parking Bay','Balcony','Ensuite','Staff Quarters',
              'Borehole','Wheelchair','Generator','CCTV','GYM','Garage','Pets Allowed',
              'Swimming Pool','Fully Furnished','Elavator']
    c1,c2,c3,c4=st.columns((1,1,1,1,))
    with st.container():
        gd,pb,bl,en=c1.checkbox(features[0]),c1.checkbox(features[1]),c1.checkbox(features[2]),c1.checkbox(features[3])
        sq,bh,wc,gn=c2.checkbox(features[4]),c2.checkbox(features[5]),c2.checkbox(features[6]),c2.checkbox(features[7])
        cc,gy,gr,pa=c3.checkbox(features[8]),c3.checkbox(features[9]),c3.checkbox(features[10]),c3.checkbox(features[11])
        sp,ff,el=c4.checkbox(features[12]),c4.checkbox(features[13]),c4.checkbox(features[14])
    c5,c6=st.columns((1,1))
    bed_r=c5.selectbox('Number of Bedrooms',bedrooms)
    if st.button('Calculate Price Range'):
        if bed_r=='Select No of bedrooms':
            st.error('Select Number of Bedrooms')
        else:
            #st.success('Price Estimation Successful')
            fetched_data={'Garden':gd,'Parking Ba':pb,'Balcony':bl,'Ensuite':en,
                          'Staff Quar':sq,'Borehole':bh,'Wheelchair':wc,
                          'Generator':gn,'CCTV':cc,'Gym':gy,'Garage':gr,
                          'Pets Allow':pa,'Swimming P':sp,'Fully Furn':ff,
                          'Elevator':el}
            checked_columns=[]
            for k in fetched_data.keys():
                if fetched_data[k]==True:
                    checked_columns.append(k)
                else:
                    continue
            checked_columns.append('bedrooms')
            checked_columns.append('Price')
            selected_data=data[checked_columns]
            selected_data.replace(['TRUE',None],[1,0],inplace=True)
            data_to_model=selected_data.apply(pd.to_numeric)
            model_v=str(multiple_model(data_to_model,bed_r))
            pred=list(model_v)
            last=pred[-5]+pred[-4]+pred[-3]+pred[-2]+pred[-1]
            if int(last)>=50000:
                v=100000-int(last)
                mean_v=int(model_v)+v
            else:
                v=int(last)
                mean_v=int(model_v)-v
            #st.subheader('Highest Price: Ksh '+str(int(mean_v*1.125)))
            #st.subheader('Lowest Price: Ksh '+str(int(mean_v*0.875)))
            st.metric(label="Estimated Price", value='Highest Price: Ksh '+str(int(mean_v*1.125)),
                      delta='Lowest Price: Ksh '+str(int(mean_v*0.875)))