# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 10:14:26 2022

@author: hp
"""


import streamlit as st
import hydralit_components as hc
from home import home
from spatial import features
from pricepred_page import main_page
from hydralit_components import HyLoader, Loaders
import time
import geopandas as gp

st.set_page_config(layout='wide',initial_sidebar_state='auto',)

menu_data = [
    {'label':"Price distribution"},#no tooltip message
    {'label':"Property Features"},
    {'label':"Estimate Price",'ttip':"Estimate price in certain Location"} #can add a tooltip message
]

over_theme = {'txc_inactive': '#FFFFFF'}
menu_id=hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home',
    hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)
nav=menu_id
data=gp.read_file('shp/buildings.shp')
if nav=='Home':
    home(data)
elif nav=='Property Features':
    st.subheader('Search for Property Features')
    regions=list(data.Region.unique())
    with st.container():
        c1,c2,c3=st.columns((1,1,1))
        reg=c1.selectbox('Region',regions)
        new_data=data[data['Region']==reg]
        bed=list(new_data.bedrooms.unique())
        bed_rooms=c2.selectbox('Bedrooms',bed)
        final_data=new_data[new_data['bedrooms']==bed_rooms]
        names=list(final_data['Name'])
        name=c3.selectbox('Name',names)
    if st.button('Submit'):
        loader=Loaders.standard_loaders
        delay=0
        with HyLoader("Loading Property Features",loader_name=loader,index=[3,0,5]):
                    time.sleep(int(delay))
                    features(geo)
elif nav=='Estimate Price':
    main_page()
