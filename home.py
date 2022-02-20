# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 08:53:11 2022

@author: Amon Melly
"""

import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def home(data):
    c1,c2,c3=st.columns((1,2,1))
    with c1:
        st.subheader("Filter Section")
        reg_list=['All']
        reg=np.array(data['Region'])
        for r in reg:
            if r in reg_list:
                continue
            else:
                reg_list.append(r)
        reg_list.sort()
        region=st.selectbox('Region',reg_list)
        if region=='All':
            beds=np.array(data['bedrooms'])
            bed_list=[]
            for b in beds:
                if b in bed_list:
                    continue
                else:
                    bed_list.append(b)
            bed_list.sort()
            bedrooms=st.selectbox('No of Bedrooms',bed_list)
        else:
            data=data[data['Region']==region]
            beds=np.array(data['bedrooms'])
            bed_list=[]
            for b in beds:
                if b in bed_list:
                    continue
                else:
                    bed_list.append(b)
            bed_list.sort()
            bedrooms=st.selectbox('No of Bedrooms',bed_list)
    with c2:
        if region=='All':
            r='Nairobi'
        else:
            r=region
        st.subheader(str(len(data))+' Houses are available for sale in '+r)
        st.map(data)
    with c3:
        st.subheader("Statistics")
        fig=plt.figure()
        st.markdown('**Number of Houses**')
        sns.countplot(data=data, x="bedrooms")
        st.pyplot(fig)
