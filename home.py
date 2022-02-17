# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 08:53:11 2022

@author: hp
"""

import streamlit as st
import geopandas as gp

def home():
    data=gp.read_file('shp/buildings.shp')
    st.map(data)