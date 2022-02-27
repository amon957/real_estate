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
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

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
    features()
elif nav=='Estimate Price':
    main_page()
