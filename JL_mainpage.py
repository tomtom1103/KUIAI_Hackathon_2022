import streamlit as st
import pandas as pd
import numpy as np
from JL_utils import *
from JL_utils2 import main_md1
from main_engine import main_engine
import pydeck as pdk

MAPBOX_API_KEY = st.secrets['map']

def main():
    #df = pd.read_pickle('data_upload/sales_eda_full.pkl')
    #heat = pd.read_pickle('data_upload/sales_eda_json_sparse.pkl')
    #seoul_df = pd.read_pickle('data_upload/seoul_coord_data.pkl')
    storetype_df = pd.read_pickle('data_upload/moneypertypeofservice.pkl')
    storetype = storetype_df['업종'].unique().tolist()

    with st.form("main1"):
        road = st.text_input("도로명주소를 입력하세요 (실험용으로 고려대로 26길 45-4 를 입력해보세요! 고대생들의 마음의 고향 춘자입니다🍺): ")
        store = st.selectbox("업종을 선택하세요: ", storetype)

        submitted = st.form_submit_button("Submit")

        if not submitted:
            st.stop()


    coords = main_engine(road,store)

    heat = pd.DataFrame(columns=(['lat','lng','eval_val']))
    for i in range(len(coords)):
        heat.loc[i,["lat","lng","eval_val"]] = coords[i][0][0], coords[i][0][1], coords[i][1]

    heat['eval_norm'] = heat['eval_val']/heat['eval_val'].max()

    layer1 = pdk.Layer(
        'ColumnLayer',
        data=heat,
        get_position='[lng, lat]',
        get_elevation='eval_norm',
        elevation_scale=1000,
        radius=15,
        get_fill_color=[255,255,255,140],
        pickable=True,
        auto_highlight=True
    )

    layer2 = pdk.Layer(
        'ColumnLayer',
        data=heat.iloc[:1],
        get_position='[lng, lat]',
        get_elevation='eval_norm',
        elevation_scale=1000,
        radius=15,
        get_fill_color=[189,27,33,255],
        pickable=True,
        auto_highlight=True
    )


    #center = [126.986, 37.565]
    center = [heat.loc[0][1], heat.loc[0][0]]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=14,
        pitch=10
        )

    tooltip = {
        "html": "위도:<b>{lat}</b>, 경도:<b>{lng}</b>, 해당 주소의 예상 매출은 <b>{eval_val}</b> 원, 주위 상권 대비 예상매출액 비율은 <b>{eval_norm}</b>.",
        "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
    }

    r = pdk.Deck(layers=[layer1,layer2],
                 map_provider='mapbox',
                 tooltip=tooltip,
                 initial_view_state=view_state)

    return r



def mainpage():
    st.subheader("Main Engine")
    st.pydeck_chart(main())
    st.markdown(main_md1)