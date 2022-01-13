import streamlit as st
import pandas as pd
import numpy as np
from JL_utils import *
from main_engine import main_engine
import pydeck as pdk
from config import map

MAPBOX_API_KEY = map

def main():
    #df = pd.read_pickle('data_upload/sales_eda_full.pkl')
    #heat = pd.read_pickle('data_upload/sales_eda_json_sparse.pkl')
    seoul_df = pd.read_pickle('data_upload/seoul_coord_data.pkl')
    storetype_df = pd.read_pickle('data_upload/moneypertypeofservice.pkl')
    storetype = storetype_df['업종'].unique().tolist()

    with st.form("main1"):
        road = st.text_input("도로명주소를 입력하세요: ")
        store = st.selectbox("업종을 선택하세요: ", storetype)

        submitted = st.form_submit_button("Submit")

        if not submitted:
            st.stop()


    st.write(main_engine(road, store))
    coords = main_engine(road,store)

    heat = pd.DataFrame(columns=(['lat','lng','eval_val']))
    for i in range(len(coords)):
        heat.loc[i,["lat","lng","eval_val"]] = coords[i][0][0], coords[i][0][1], coords[i][1]

    layer = pdk.Layer(
        'HeatmapLayer',
        heat,
        get_position='[lng, lat]',
        get_weight='eval_val'
    )

    #center = [126.986, 37.565]
    center = [heat.loc[0][1], heat.loc[0][0]]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=14)

    r = pdk.Deck(layers=[layer],
                 map_provider='mapbox',
                 initial_view_state=view_state)

    return r



def mainpage():
    st.subheader("Main Engine")

    st.pydeck_chart(main())
