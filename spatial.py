# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 11:08:58 2022

@author: hp
"""

import geopandas as gp
import osmnx as ox
from shapely.geometry import LineString
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium
from hydralit_components import HyLoader, Loaders
import time
import branca


def search_amenity_within(building,amenity_type,dist):
    building=building.to_crs('EPSG:21037')
    amenity_type=amenity_type.to_crs('EPSG:21037')
    len_df=0
    dist=dist
    while len_df==0:
        if dist<4000:
            buffer=building.buffer(dist)
            df=gp.GeoDataFrame(geometry=buffer,crs='EPSG:21037')
            subset=gp.sjoin(amenity_type,df, how='inner', predicate='within')
            len_df=len(subset)
            dist=dist+500
        else:
            subset=pd.DataFrame()
            len_df=1
    return(subset)
def features():
    c1,c2=st.columns((2,1))
    with c1:
        st.text('Enter Id between 1 & 1000')
        p_id=st.text_input("Enter Property Id")
        loc_f=st.checkbox('Location Features (Distance to Utilities)')
        build_f=st.checkbox('Building Features')
        if st.button('Submit'):
            loader=Loaders.standard_loaders
            delay=0
            with HyLoader("Loading Property Id {}".format(p_id),loader_name=loader,index=[3,0,5]):
                    time.sleep(int(delay))
                    houses=gp.read_file('shp/buildings.shp')
                    geo=houses[houses['b_id']==int(p_id)]

                    layers={'fuel':'shp/fuel.shp','hos':'shp/hospital.shp','malls':'shp/malls.shp','pharm':'shp/pharmacy.shp',
                        'church':'shp/place_of_worship.shp','police':'shp/police.shp','school':'shp/school.shp'}
                    buffer_dist={'fuel':1000,'hos':1000,'malls':1500,'pharm':3000,
                        'church':1000,'police':2000,'school':1000}
                    facility_type_names={'fuel':'Gas Station','hos':'Hospital','malls':'Shopping Mall','pharm':'Pharmacy',
                        'church':'Place of Worship','police':'Police Station','school':'School'}

                    facility_type=[]
                    facility_name=[]
                    minimum_dist=[]
                    layers_to_map=[]
    
                    for layer in list(layers.keys()):
                        shp=gp.read_file(layers[layer])
                        subset=search_amenity_within(geo,shp,buffer_dist[layer])
                        if len(subset)==0:
                            facility_type.append(facility_type_names[layer])
                            facility_name.append('Not Available')
                            minimum_dist.append('More than 4 KM Away')
                        else:
                            building=geo.to_crs('EPSG:21037')
                            names=list(subset['name'])
                            geom=list(subset['geometry'])
                            x_utility=list(subset['y_coord'])
                            y_utility=list(subset['x_coord'])
                            length=[]
                            for k in range(len(geom)):
                                length.append(np.array(list(gp.GeoSeries(geom[k]).distance(building,align=False)))[0])
                            l=round(np.array(length).min()/1000,2)
                            ind=length.index(np.array(length).min())
                            layers_to_map.append({'layer':layer,'x':x_utility[ind],'y':y_utility[ind],'name':names[ind]})
                            facility_type.append(facility_type_names[layer])
                            facility_name.append(names[ind])
                            minimum_dist.append(str(l)+' KM')
    
                    school = folium.FeatureGroup(name='Nearest School')
                    fuel = folium.FeatureGroup(name='Nearest Gas Station')
                    church = folium.FeatureGroup(name='Nearest Church')
                    mall = folium.FeatureGroup(name='Nearest Mall')
                    police = folium.FeatureGroup(name='Nearest Police Station')
                    pharmacy = folium.FeatureGroup(name='Nearest Pharmacy')
                    hospital = folium.FeatureGroup(name='Nearest Hospital')
                    house = folium.FeatureGroup(name='Property for Sale')
                    fig=branca.element.Figure(width="100%")
                    m=folium.Map(location=[np.array(geo['lat'])[0],np.array(geo['lon'])[0]],zoom_start=14)
                    folium.TileLayer(
                        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                        attr = 'Esri',
                        name = 'Esri Satellite',
                        overlay = False,
                        control = True
                    ).add_to(m)
                    folium.Marker([np.array(geo['lat'])[0],np.array(geo['lon'])[0]], tooltip=np.array(geo['Name'])[0]).add_to(house)
                    folium.Circle([np.array(geo['lat'])[0],np.array(geo['lon'])[0]],100, fill=False,color='red').add_to(house)
                    for j in range(len(layers_to_map)):
                        l=layers_to_map[j]['layer']
                        if l=='fuel':
                            folium.Marker([layers_to_map[j]['x'],layers_to_map[j]['y']],icon=folium.Icon(color='red',icon_color='#FFFF00')).add_to(fuel)
                        elif l=='hos':
                            folium.Marker([layers_to_map[j]['x'],layers_to_map[j]['y']],icon=folium.Icon(color='gray',icon_color='#FFFF00')).add_to(hospital)
                        elif l=='malls':
                            folium.Marker([layers_to_map[j]['x'],layers_to_map[j]['y']],icon=folium.Icon(color='green',icon_color='#FFFF00')).add_to(mall)
                        elif l=='pharm':
                            folium.Marker([layers_to_map[j]['x'],layers_to_map[j]['y']],icon=folium.Icon(color='blue',icon_color='#FFFF00')).add_to(pharmacy)
                        elif l=='church':
                            folium.Marker([layers_to_map[j]['x'],layers_to_map[j]['y']],icon=folium.Icon(color='black',icon_color='#FFFF00')).add_to(church)
                        elif l=='police':
                            folium.Marker([layers_to_map[j]['x'],layers_to_map[j]['y']],icon=folium.Icon(color='yellow',icon_color='#FFFF00')).add_to(police)
                        elif l=='school':
                            folium.Marker([layers_to_map[j]['x'],layers_to_map[j]['y']],icon=folium.Icon(color='blue',icon_color='#FFFF00')).add_to(school)
                    m.add_child(house)
                    m.add_child(fuel)
                    m.add_child(school)
                    m.add_child(church)
                    m.add_child(mall)
                    m.add_child(police)
                    m.add_child(hospital)
                    m.add_child(pharmacy)
                    m.add_child(folium.map.LayerControl())
                    fig.add_child(m)
                    properties=pd.DataFrame()
                    properties['Type']=facility_type
                    properties['Name']=facility_name
                    properties['Distance']=minimum_dist
                    index=[1,2,3,4,5,6,7]
                    properties['SNo.']=index
                    loc_properties=properties.set_index('SNo.',drop=True)
    
                    other_properties=geo.dropna(axis=1,how='all')
                    other_properties=other_properties.drop(['geometry'],axis='columns', inplace=True)
    
                    with c1:
                        st.subheader(np.array(geo['Name'])[0])
                        folium_static(m)
                    with c2:
                        st.dataframe(loc_properties)
                        st.text('Building Features')
                        st.dataframe(other_properties)
